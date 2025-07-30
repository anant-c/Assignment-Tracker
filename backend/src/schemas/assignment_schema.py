from pydantic import BaseModel, Field,  UUID4, NonNegativeInt
from datetime import date, datetime, time, timedelta


class assignment_service(BaseModel):
    name: str
    description: str | None = None
    teacher_id: UUID4 

class update_assignment_service(BaseModel):
    name: str | None = None
    description: str | None = None

class assignment(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    status: str | None = None
    asssignment_service_id: UUID4

class question(BaseModel):
    text: str
    assignment_id: UUID4

class answer(BaseModel):
    question_id: UUID4
    answer_text: str | None
    asssignment_service_id: UUID4
    student_id: UUID4


class result(BaseModel):
    student_id: UUID4
    assignment_id: UUID4
    score: NonNegativeInt | None = None
    feedback: str | None = None
    




