import os
from sqlalchemy.orm import Session
from models.db_models import Teacher, AssignmentService
from fastapi import HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

def create_teacher(db: Session, username: str, first_name: str, last_name: str, role: str, mobile: str , college: str, email: str, password: str):
    if(not username or not first_name or not last_name or not role or not college or not email or not password):
        raise ValueError("All fields are required")

    if(db.query(Teacher).filter(Teacher.username == username.strip()).first()):
        raise ValueError("Username already exists")

    if(db.query(Teacher).filter(Teacher.email == email.strip()).first()):
        raise ValueError("Email already exists")
    
    # Hash the password
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = password_context.hash(password)

    new_teacher = Teacher(
        username=username,
        first_name=first_name,
        last_name=last_name,
        role=role,
        mobile=mobile,
        college=college,
        email=email,
        password=hashed_password
    )
    token = jwt.encode({"sub": new_teacher.username}, os.getenv("JWT_SECRET_KEY"), algorithm= os.getenv("JWT_ALGO"))
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    
    return {"message": "Teacher created successfully", "token": token, "teacher_id": str(new_teacher.id)}


def signinTeacher(email: str, password: str, db: Session):
    if not email or not password:
        raise ValueError("Email and password are required")

    teacher = db.query(Teacher).filter(Teacher.email == email.strip()).first()
    if not teacher:
        raise ValueError("Invalid email or password")

    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not password_context.verify(password, teacher.password):
        raise ValueError("Invalid password")

    token = jwt.encode({"sub": teacher.username}, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGO"))
    
    return {"message": "Signin successful", "token": token, "teacher_id": str(teacher.id)}


def update_teacher_profile(id, updateTeacher, db, username):
    print(f"Authenticated teacher: {username}")

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Ensure the authenticated teacher can only update their own profile
    if(username != db.query(Teacher).filter(Teacher.id == id).first().username):
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")


    # Update only the fields that are provided in the request
    for key, value in updateTeacher.dict(exclude_unset=True).items():
        if value is not None:
            if key == "password":
                # Hash the password if it's being updated
                password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                value = password_context.hash(value)

            setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher

def create_assignment_service(name, description, teacher_id, db, username):
    """
    Create a new assignment service.
    Requires teacher authentication.
    """
    print(f"Authenticated teacher: {username}")
    new_service = AssignmentService(
        name=name,
        description=description,
        teacher_id=teacher_id
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)


    return {"message": f"Assignment service {new_service.id} created successfully by", "teacher: ": username}

