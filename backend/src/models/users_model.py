from sqlalchemy import Column, ForeignKey, Integer, String, relationship, Table
from sqlalchemy.dialects.postgresql import UUID
from conf.db import Base

student_assignment_service = Table(
    'student_assignment_service',
    Base.metadata,
    Column('student_id', UUID(as_uuid=True), ForeignKey('students.id'), primary_key=True),
    Column('assignment_service_id', UUID(as_uuid=True), ForeignKey('assignment_services.id'), primary_key=True)
)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
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

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
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