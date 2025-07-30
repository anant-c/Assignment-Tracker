import os
from sqlalchemy.orm import Session
from models.db_models import Student
from passlib.context import CryptContext
from schemas.student_schema import StudentCreate, StudentUpdate, StudentSignin
import jwt
from uuid import UUID
from fastapi import HTTPException, Depends
from jwt.exceptions import InvalidTokenError

def create_student(db: Session, student: StudentCreate):
    if(not student.username or not student.first_name or not student.last_name or not student.role or not student.college or not student.email or not student.password):
        raise ValueError("All fields are required")

    if(db.query(Student).filter(Student.username == student.username.strip()).first()):
        raise ValueError("Username already exists")

    if(db.query(Student).filter(Student.email == student.email.strip()).first()):
        raise ValueError("Email already exists")
    
    # Hash the password
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = password_context.hash(student.password)

    new_student = Student(
        username=student.username,
        first_name=student.first_name,
        last_name=student.last_name,
        role=student.role,
        mobile=student.mobile,
        college=student.college,
        email=student.email,
        password=hashed_password
    )
    token = jwt.encode({"sub": new_student.username}, os.getenv("JWT_SECRET_KEY"), algorithm= os.getenv("JWT_ALGO"))
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {"message": "Student created successfully", "token": token, "student_id": str(new_student.id)}

def signinStudent(email: str, password: str, db: Session): 
    if not email or not password:
        raise ValueError("Email and password are required")

    student = db.query(Student).filter(Student.email == email.strip()).first()
    if not student:
        raise ValueError("Invalid email or password")

    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not password_context.verify(password, student.password):
        raise ValueError("Invalid password")

    token = jwt.encode({"sub": student.username}, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGO"))

    return {"message": "Signin successful", "token": token, "student_id": str(student.id)}

def update_student_profile(id:UUID, updateStudent: StudentUpdate, db: Session, username: str):
    print(f"Authenticated student: {username}")

    if not username:
        raise HTTPException(status_code= 401, detail="Unauthorized")
    
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Ensure the authenticated user is the one owner of this account to modify
    if( username != db.query(Student).filter(Student.id == id).first().username):
        raise HTTPException(status_code=403, detail= "Not authorized to update this account.")
    

    for key,value in updateStudent.dict(exclude_unset=True).items():
        if value is not None:
            if(key == "password"):
                password_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
                value = password_context.hash(value)
            
            setattr(student, key, value)

    
    db.commit()
    db.refresh(student)
    
    return student