from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class Teacher(BaseModel):
    id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    role: Literal['teacher'] = 'teacher'    
    password: str = Field(..., min_length=8, max_length=128)
    assignments_services_ids: List[UUID] = Field(default_factory=list)  
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = Field(None, regex=r'^\+?[1-9]\d{1,14}$')
    college: str = Field(..., min_length=1, max_length=100)

class Student(Teacher):
    role: Literal['student'] = 'student'  
