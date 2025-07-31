from fastapi import APIRouter, Depends, HTTPException
from models.db_models import Teacher, Student
from controllers.teacher_controller import create_teacher , signinTeacher, update_teacher_profile, create_assignment_service, update_assigment_service, delete_assignment_services_byTeacher
from controllers.student_controller import create_student, signinStudent , update_student_profile
from controllers.assignment_controller import fetch_assignment_services_byTeacher, fetch_assignment_service_using_id
from schemas.teacher_schema import TeacherCreate, TeacherUpdate, TeacherSignin
from schemas.student_schema import StudentCreate, StudentSignin, StudentUpdate
from schemas.assignment_schema import assignment_service, update_assignment_service ,assignment, question, answer, result
from sqlalchemy.orm import Session
from conf.db import get_db
from uuid import UUID
from middlewares.student_authMiddleware import verify_student
from middlewares.teacher_authMiddleware import verify_teacher
from middlewares.user_authMiddleware import verify_user

signup_router = APIRouter()
signin_router = APIRouter() 
student_router = APIRouter()
teacher_router = APIRouter()
assignment_router = APIRouter()


@signup_router.post("/teachers/")
def signup_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    teacher.role = "teacher"  # Ensure the role is set to teacher
    return create_teacher(
        db,
        teacher=teacher
    )


@signin_router.post("/teachers/")   
def signin_teacher(teacher: TeacherSignin, db: Session = Depends(get_db)):
    return signinTeacher(
        email=teacher.email,
        password=teacher.password,
        db=db
    )

@teacher_router.put("/teachers/{id}")
def update_teacher_profile(id: UUID, updateTeacher: TeacherUpdate, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    """
    Update teacher profile by ID.
    Requires teacher authentication.
    """
    return update_teacher_profile(id, updateTeacher, db, username)

@teacher_router.get("/fetch-students")
def fetch_students(db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    """
    Fetch all students.
    Requires teacher authentication.
    """
    print(f"Authenticated teacher: {username}")
    return db.query(Student).all()

@teacher_router.get("/fetch-students/{id}")
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

@assignment_router.post("/create-service")
def create_service(assignment_service: assignment_service, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    """
    Create a service for the teacher.
    Requires teacher authentication.
    """
    print(f"Authenticated teacher: {username}")
    # Logic to create a service can be added here

    return create_assignment_service(
        assignment_service.name,
        assignment_service.description,
        teacher_id=assignment_service.teacher_id,
        db=db,
        username=username
    )

@assignment_router.put("/services/{id}")
def edit_service(id: UUID, update_service: update_assignment_service, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    return update_assigment_service(id, update_service,db, username)

# -------------------------------------------------------------------------------------------ASSIGNMENT ROUTES-------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------ASSIGNMENT ROUTES-------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------ASSIGNMENT ROUTES-------------------------------------------------------------------------------------------


@assignment_router.get("/services/byteacher/{id}")
def get_assignment_services_using_teacher_id(id: UUID, db: Session= Depends(get_db), username: str= Depends(verify_user)):
    return fetch_assignment_services_byTeacher(id, db, username)

@assignment_router.delete("/services/byteacher/{id}")
def delete_assignment_services_using_teacher_id(id: UUID, db: Session= Depends(get_db), username: str= Depends(verify_teacher)):
    return delete_assignment_services_byTeacher(id, db, username)

@assignment_router.get("/services/{id}")
def get_assignment_service_using_id(id:UUID, db: Session= Depends(get_db), username: str=Depends(verify_user)):
    return fetch_assignment_service_using_id(id, db, username)

# -------------------------------------------------------------------------------------------STuDENT ROUTES------------------------------------------------------------------------------------------- 
# -------------------------------------------------------------------------------------------STUDENT ROUTES-------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------STUDENT ROUTES-------------------------------------------------------------------------------------------

@signup_router.post("/students/")
def signup_student(student: StudentCreate, db: Session = Depends(get_db)):
    student.role = "student"  # Ensure the role is set to student
    return create_student(
        db,
        student=student
    )

@signin_router.post("/students/")
def signin_student(student: StudentSignin, db: Session = Depends(get_db)):
    return signinStudent(
        email=student.email,
        password=student.password,
        db=db
    )

@student_router.put("/students/{id}")
def update_student_profile(id: UUID, updateStudent: StudentUpdate, db: Session = Depends(get_db), username: str = Depends(verify_student)):
    """
    Update student profile by ID.
    Requires student authentication.
    """
    return update_student_profile(id, updateStudent, db, username)


@student_router.get("/fetch-teachers")
def fetch_teachers(db: Session = Depends(get_db), username: str = Depends(verify_student)):
    """
    Fetch all teachers.
    Requires student authentication.
    """
    print(f"Authenticated student: {username}")
    return db.query(Teacher).all()

@student_router.get("/fetch-teachers/{id}")
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