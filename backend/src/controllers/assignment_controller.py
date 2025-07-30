import os
from sqlalchemy.orm import Session
from models.db_models import Teacher, AssignmentService
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