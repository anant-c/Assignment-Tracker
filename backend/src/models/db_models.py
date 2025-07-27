from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.dialects.postgresql import UUID
from conf.db import Base
from sqlalchemy.orm import relationship
import uuid

student_assignment_service = Table(
    'student_assignment_service',
    Base.metadata,
    Column('student_id', UUID(as_uuid=True), ForeignKey('students.id'), primary_key=True),
    Column('assignment_service_id', UUID(as_uuid=True), ForeignKey('assignment_services.id'), primary_key=True)
)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False) 
    mobile = Column(String, nullable=True)
    college = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    assignment_services = relationship("AssignmentService", back_populates="teacher")


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False) 
    mobile = Column(String, nullable=True)
    college = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    answers = relationship("Answer", back_populates="student")
    results = relationship("Result", back_populates="student")
    assignment_services = relationship("AssignmentService", secondary=student_assignment_service, back_populates="students")


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    text = Column(String, nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)

    answers = relationship("Answer", back_populates="question") 
    assignment = relationship("Assignment", back_populates="questions")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    answer = Column(String, nullable=True)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)

    question = relationship("Question", back_populates="answers")
    student = relationship("Student", back_populates="answers")
    assignment = relationship("Assignment", back_populates="answers")


class Result(Base):
    __tablename__ = "results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
    score = Column(Integer, nullable=True)  # Score can be null if not graded yet
    feedback = Column(String, nullable=True)

    student = relationship("Student", back_populates="results")
    assignment = relationship("Assignment", back_populates="results")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)  
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True, index=True, default=None)
    status = Column(String, nullable=False, default="pending")  # pending, completed, overdue
    assignment_service_id = Column(UUID(as_uuid=True), ForeignKey("assignment_services.id"), nullable=False)

    questions = relationship("Question", back_populates="assignment")
    answers = relationship("Answer", back_populates="assignment")
    results = relationship("Result", back_populates="assignment")
    assignment_service = relationship("AssignmentService", back_populates="assignments")


class AssignmentService(Base):
    __tablename__ = "assignment_services"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="assignment_services")
    students = relationship("Student", secondary=student_assignment_service, back_populates="assignment_services")
    assignments = relationship("Assignment", back_populates="assignment_service")