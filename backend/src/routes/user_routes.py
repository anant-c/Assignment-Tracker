from fastapi import APIRouter, Depends, HTTPException
from models.db_models import Teacher, Student
from controllers.teacher_controller import create_teacher , signinTeacher, update_teacher_profile
from controllers.student_controller import create_student, signinStudent , update_student_profile
from schemas.teacher_schema import TeacherCreate, TeacherUpdate, TeacherSignin
from schemas.student_schema import StudentCreate, StudentSignin, StudentUpdate
from sqlalchemy.orm import Session
from conf.db import get_db
from uuid import UUID
from middlewares.student_authMiddleware import verify_student
from middlewares.teacher_authMiddleware import verify_teacher


signup_router = APIRouter()
signin_router = APIRouter() 
student_router = APIRouter()
teacher_router = APIRouter()


@signup_router.post("/teachers/")
def signup_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    teacher.role = "teacher"  # Ensure the role is set to teacher
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


@signin_router.post("/teachers/")
def signin_teacher(teacher: TeacherSignin, db: Session = Depends(get_db)):
    return signinTeacher(
        email=teacher.email,
        password=teacher.password,
        db=db
    )

@teacher_router.put("/{id}")
def update_profile(id: UUID, updateTeacher: TeacherUpdate, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    """
    Update teacher profile by ID.
    Requires teacher authentication.
    """
    return update_teacher_profile(id, updateTeacher, db, username)

@teacher_router.get("/")
def fetch_students(db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    """
    Fetch all students.
    Requires teacher authentication.
    """
    print(f"Authenticated teacher: {username}")
    return db.query(Student).all()

@teacher_router.get("/{id}")
def fetch_student_by_id(id: UUID, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    """
    Fetch a student by ID.
    Requires teacher authentication.
    """
    print(f"Authenticated teacher: {username}")
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@teacher_router.post("/")
def create_service(db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    """
    Create a service for the teacher.
    Requires teacher authentication.
    """
    print(f"Authenticated teacher: {username}")
    # Logic to create a service can be added here
    


    return {"message": "Service created successfully", "teacher": username}

# -------------------------------------------------------------------------------------------STuDENT ROUTES------------------------------------------------------------------------------------------- 
# -------------------------------------------------------------------------------------------STUDENT ROUTES-------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------STUDENT ROUTES-------------------------------------------------------------------------------------------

@signup_router.post("/students/")
def signup_student(student: StudentCreate, db: Session = Depends(get_db)):
    student.role = "student"  # Ensure the role is set to student
    return create_student(
        db,
        student.username,
        student.first_name,
        student.last_name,
        student.role,
        student.mobile,
        student.college,
        student.email,
        student.password
    )

@signin_router.post("/students/")
def signin_student(student: StudentSignin, db: Session = Depends(get_db)):
    return signinStudent(
        email=student.email,
        password=student.password,
        db=db
    )

@student_router.put("/{id}")
def update_profile(id: UUID, updateStudent: StudentUpdate, db: Session = Depends(get_db), username: str = Depends(verify_student)):
    """
    Update student profile by ID.
    Requires student authentication.
    """
    return update_student_profile(id, updateStudent, db, username)


@student_router.get("/")
def fetch_teachers(db: Session = Depends(get_db), username: str = Depends(verify_student)):
    """
    Fetch all teachers.
    Requires student authentication.
    """
    print(f"Authenticated student: {username}")
    return db.query(Teacher).all()

@student_router.get("/{id}")
def fetch_teacher_by_id(id: UUID, db: Session = Depends(get_db), username: str = Depends(verify_student)):
    """
    Fetch a teacher by ID.
    Requires student authentication.
    """
    print(f"Authenticated student: {username}")
    teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher