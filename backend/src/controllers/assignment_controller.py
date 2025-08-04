import os
from sqlalchemy.orm import Session
from models.db_models import Teacher, AssignmentService, Student, Assignment, Question, Answer, Result
from fastapi import HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


def fetch_assignment_services_byTeacher(id: UUID, db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    services = db.query(AssignmentService).filter(AssignmentService.teacher_id == id).all()
    teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not services:
        raise HTTPException(status_code=404, detail=f"No services for {teacher} teacher found.")
    
    return {
        "message": f"{teacher} Teacher's assignment services fetched successfully.",
        "services": services
    }

def fetch_assignment_service_using_id(id: UUID, db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    service = db.query(AssignmentService).filter(AssignmentService.id == id).all()

    if not service:
        raise HTTPException(status_code=404, detail=f"No service found by id: {id}")
    
    return {
        "message": f"Successfully found the service with id: {id}",
        "service": service
    }

def fetch_students_subscribedTo_a_service(id:UUID, db:Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    service = db.query(AssignmentService).filter(AssignmentService.id == id).first()

    if not service:
        raise HTTPException(status_code=404, detail=f"Assignment Service {id} not found.")
    
    subscribed_students = service.students

    if not subscribed_students:
        raise HTTPException(status_code=404, detail="No subscribed students found")

    return [
        {
            "id": str(student.id),
            "username": student.username,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
        }
        for student in subscribed_students
    ]

def fetch_assignment_service_subcribedBy_a_student(id:UUID, db:Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail=f"Student {id} not found.")

    assignment_services = student.assignment_services

    if not assignment_services:
        raise HTTPException(status_code=404, detail=f"No assignment_services found for student {student.first_name}")

    return {
        "message": f"Fetched all subscribed services by student {student.first_name}.",
        "assignment_services" : assignment_services
    }

def get_assignment_by_id(id:UUID, db:Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    assignment = db.query(Assignment).filter(Assignment.id == id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail=f"Assignment with id:{id} not found.")
    
    return {
        "message": "Successfully fetched the assignment.",
        "assignment": assignment
    }

def get_questions_from_assignment(id: UUID, db: Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    questions = db.query(Question).filter(Question.assignment_id == id).all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found.")
    
    return {
        "message": "Question fetched successfully.",
        "questions": questions
    }

def get_questions_using_id(id: UUID, db: Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    question = db.query(Question).filter(Question.id == id).first()

    if not question:
        raise HTTPException(status_code=404, detail= f"Question with id:{id} not found.")
    
    return {
        "question": question
    }

def get_answers_of_question(id:UUID, db: Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    answers = db.query(Answer).filter(Answer.question_id == id).all()

    if not answers:
        raise HTTPException(status_code=404, detail=f"No answers found for question: {id}")

    return {
        "message" : "Answer fetched successfully.",
        "answers": answers
    }

def get_answers_using_id(id:UUID, db:Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    answer = db.query(Answer).filter(Answer.id == id).first()

    if not answer:
        raise HTTPException(status_code=404, detail= f"Answer with id:{id} not found.")
    
    return {
        "answer": answer
    }

def get_answers_by_student(id1:UUID, id2: UUID,id3:UUID ,db: Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    student = db.query(Student).filter(Student.id == id1).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with username {student.username} not found.")
    
    assignment_service = db.query(AssignmentService).filter(AssignmentService.id == id2).first()

    if not assignment_service:
        raise HTTPException(status_code=404, detail="Assignment service to which the answers are requested is not found.")

    assignment = db.query(Assignment).filter(Assignment.id == id3).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment to which the answers are requested is not found.")
    
    
    answers = db.query(Answer).filter(
        Answer.student_id == id1,
        Answer.assignment_id == id3
        ).all()

    return {
        "message": f"Answers fetched for all the questions in assignment id: {id3} by student username: {student.username}",
        "answers": answers
    }

def get_answers_to_assignment(id: UUID, db:Session, username:str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    assignment = db.query(Assignment).filter(Assignment.id == id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found for the answers.")
    
    answers = db.query(Answer).filter(Answer.assignment_id == id).all()

    if not answers:
        raise HTTPException(status_code=404, detail=f"No answers found for this assignment id:{id}")


    return {
        "message": f"Answers for assignment id: {id} fetched successfully.",
        "answers": answers
    }

def get_results_to_assignment(id:UUID, db: Session, username:str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    results = db.query(Result).filter(Result.assignment_id== id).all()

    if not results:
        raise HTTPException(status_code=404, detail=f"No results found for the assignment with id: {id}")
    
    return {
        "message": "Results fetched successfully for the assignment.",
        "results": results
    }

def get_results_by_id(id:UUID, db:Session , username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = db.query(Result).filter(Result.id == id).first()

    if not result:
        raise HTTPException(status_code=404, detail="Result not found.")
    
    return {
        "message": "Result fetched successfully.",
        "result" : result
    }