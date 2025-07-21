from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class result(BaseModel):
    id: UUID
    student_id: UUID
    assignment_id: UUID
    score: Optional[float] = Field(None, ge=0, le=100)  # Score between 0 and 100
    feedback: Optional[str] = Field(None, max_length=500)  # Feedback from the teacher

class answer(BaseModel):
    id: UUID
    question: UUID
    answer: str = Field(..., min_length=1, max_length=500)  # Answer text
    student_id: UUID
    assignment_id: UUID
    submitted_at: Optional[str] = Field(None, regex=r'^\d{4}-\d{2}-\d{2}$')  # YYYY-MM-DD format

class question(BaseModel):
    id: UUID
    text: str = Field(..., min_length=1, max_length=500)  # Question text
    type: Literal['multiple_choice', 'short_answer', 'essay']  # Type of question
    options: Optional[List[str]] = Field(None, min_length=2, max_length=5)  # Options for multiple choice questions
    correct_answer: Optional[str] = Field(None, max_length=500)  # Correct answer for the question

class assignments(BaseModel):
    id: UUID
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    questions: List[question] = Field(default_factory=list)  # List of questions in the assignment
    answers: List[answer] = Field(default_factory=list)  # List of answers for the questions
    due_date: Optional[str] = Field(None, regex=r'^\d{4}-\d{2}-\d{2}$')  # YYYY-MM-DD format
    status: Literal['pending', 'completed', 'overdue'] = 'pending'
    teacher_id: UUID
    student_ids: List[UUID] = Field(default_factory=list)  # List of student IDs
    

class assignmentService(BaseModel):
    id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    teacher_id: UUID
    assignments = List[UUID] = Field(default_factory=list)  # List of assignment IDs