import os
from sqlalchemy.orm import Session
from models.db_models import Teacher, AssignmentService, Student
from fastapi import HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
import jwt
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
