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
    asssignment_service_id: UUID4 | None = None

class assignment_update(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    status: str | None = None

class question(BaseModel):
    text: str
    assignment_id: UUID4 | None = None

class question_update(BaseModel):
    text: str | None = None

class answer(BaseModel):
    question_id: UUID4 | None = None
    answer_text: str | None = None
    asssignment_service_id: UUID4 | None = None
    student_id: UUID4 | None = None


class result(BaseModel):
    student_id: UUID4 | None = None
    assignment_id: UUID4 | None = None
    score: NonNegativeInt | None = None
    feedback: str | None = None

class resultUpdate(BaseModel):
    score: NonNegativeInt
    feedback: str | None = None
    




