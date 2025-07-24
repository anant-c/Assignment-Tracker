from fastapi import APIRouter, Depends
from controllers.teacher_controller import create_teacher
from pydantic import BaseModel
from sqlalchemy.orm import Session
from conf.db import get_db

router = APIRouter()

class TeacherCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str
    mobile: str | None = None
    college: str
    email: str
    password: str

@router.post("/teachers/")
def signup_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    return create_teacher(
        db,
        teacher.username,
        teacher.first_name,
        teacher.last_name,
        teacher.role,
        teacher.mobile,
        teacher.college,
        teacher.email,
        teacher.password
    )

