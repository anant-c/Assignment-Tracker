import os
from sqlalchemy.orm import Session
from models.db_models import Student
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

def create_student(db: Session, username: str, first_name: str, last_name: str, role: str, mobile: str , college: str, email: str, password: str):
    if(not username or not first_name or not last_name or not role or not college or not email or not password):
        raise ValueError("All fields are required")

    if(db.query(Student).filter(Student.username == username.strip()).first()):
        raise ValueError("Username already exists")

    if(db.query(Student).filter(Student.email == email.strip()).first()):
        raise ValueError("Email already exists")
    
    # Hash the password
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = password_context.hash(password)

    new_student = Student(
        username=username,
        first_name=first_name,
        last_name=last_name,
        role=role,
        mobile=mobile,
        college=college,
        email=email,
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