import os
from sqlalchemy.orm import Session
from models.db_models import Student, AssignmentService, Question, Assignment, Answer, Result
from passlib.context import CryptContext #type: ignore
from schemas.student_schema import StudentCreate, StudentUpdate, StudentSignin
from schemas.assignment_schema import answer
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

# new thing i learnt, how to post in many-to-many using sqlalchemy orm
def subscribe_assignmentService(id: UUID, db: Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    student = db.query(Student).filter(Student.username == username).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    service = db.query(AssignmentService).filter(AssignmentService.id == id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Assignment Service not found.")
    
    # Check if the student is already subscribed:
    if service in student.assignment_services:
        return {
            "message": f"User: {username} is already subscribed to Assignment Service: {service.name}"
        }

    # Add the subscription - append the service to student's assignment_services list
    student.assignment_services.append(service)

    db.commit()
    db.refresh(student)

    return {
        "message": f"User: {username} subscribed successfully to Assignment Service: {service.name}"
    }

def post_answer(id: UUID, answer: answer, db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="User not found.")
    
    question = db.query(Question).filter(Question.id == id).first()

    if not question:
        raise HTTPException(status_code=404, detail= "Question not found.")
    
    assignment_id = question.assignment_id

    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment for the question not found.")
    
    service_id = assignment.assignment_service_id

    service = db.query(AssignmentService).filter(AssignmentService.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Assignment Service for this question not found.")
    
    student = db.query(Student).filter(Student.username == username).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    #------------ACCESS CHECK HERE---------------
    if service not in student.assignment_services:
        raise HTTPException(status_code=403, detail=f"Student {student.username} haven't subscribed to the assignment service for this question. So, cann't post answers to the question.")
    
    new_answer = Answer(
        question_id= id,
        answer= answer.answer_text,
        assignment_id= assignment_id,
        student_id = student.id
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return {
        "message": f"Answer: {new_answer.id} submitted successfully to Question: {id}.",
        "answer": new_answer
    }

def get_student_result(id:UUID, db:Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    results = db.query(Result).filter(Result.student_id==id).all()

    if not results:
        raise HTTPException(status_code=404, detail=f"Results not found for student with id {id}")

    return {
        "message": f"Results successfully fetched for student with id: {id}",
        "result": results
    }