from fastapi import APIRouter, Depends, HTTPException
from models.db_models import Teacher, Student, Assignment
from controllers.teacher_controller import create_teacher , signinTeacher, update_teacher_profile, create_assignment_service, update_assigment_service, delete_assignment_services_byTeacher, post_assignments, update_assignment, delete_assignment, post_questions, update_question, delete_question, create_result, update_result
from controllers.student_controller import create_student, signinStudent , update_student_profile, subscribe_assignmentService, post_answer, get_student_result
from controllers.assignment_controller import fetch_assignment_services_byTeacher, fetch_assignment_service_using_id, fetch_students_subscribedTo_a_service, fetch_assignment_service_subcribedBy_a_student, get_assignment_by_id, get_questions_from_assignment, get_questions_using_id, get_answers_of_question, get_answers_using_id, get_answers_by_student, get_answers_to_assignment, get_results_to_assignment, get_results_by_id
from schemas.teacher_schema import TeacherCreate, TeacherUpdate, TeacherSignin
from schemas.student_schema import StudentCreate, StudentSignin, StudentUpdate
from schemas.assignment_schema import assignment_service, update_assignment_service ,assignment, assignment_update,question, question_update,answer, result, resultUpdate
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

@teacher_router.post("/services/{id}/assignments")
def create_assignment(id: UUID, create_assignments: assignment, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    return post_assignments(id, create_assignments, db, username)

@teacher_router.put("/assignments/{id}")
def edit_assignment(id:UUID, assignment_update: assignment_update, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):

    return update_assignment(id, assignment_update, db, username)

@teacher_router.delete("/assignments/{id}")
def delete_assignments_by_teacher(id:UUID, db: Session= Depends(get_db), username: str = Depends(verify_teacher)):
    return delete_assignment(id, db, username)

@teacher_router.post("/assignment-service/assignment/{id}/question")
def create_questions(id:UUID, question: question, db: Session=Depends(get_db), username: str = Depends(verify_teacher)):
    return post_questions(id, question, db, username)

@teacher_router.put("/assignment-services/assignment/question/{id}")
def edit_questions(id:UUID, question_edit: question_update, db: Session=Depends(get_db), username: str=Depends(verify_teacher)):
    return update_question(id, question_edit, db, username)

@teacher_router.delete("/assignment-services/assignment/question/{id}")
def delete_question_by_teacher(id:UUID, db: Session=Depends(get_db), username: str=Depends(verify_teacher)):
    return delete_question(id, db, username)

@teacher_router.post("/assignment-services/assignment/{id1}/student/{id2}/result")
def post_result(id1:UUID, id2:UUID, result: result ,db:Session=Depends(get_db), username= Depends(verify_teacher)):
    return create_result(id1,id2, result,db, username)

@teacher_router.put("/results/{id}")
def edit_result(id:UUID,result: resultUpdate , db:Session= Depends(get_db), username = Depends(verify_teacher)):

    return update_result(id, result, db, username)


# -------------------------------------------------------------------------------------------ASSIGNMENT ROUTES-------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------ASSIGNMENT ROUTES-------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------ASSIGNMENT ROUTES-------------------------------------------------------------------------------------------


@assignment_router.get("/teachers/{id}/assignment-services")
def get_assignment_services_using_teacher_id(id: UUID, db: Session= Depends(get_db), username: str= Depends(verify_user)):
    return fetch_assignment_services_byTeacher(id, db, username)

@assignment_router.delete("/assignment-services/{id}")
def delete_assignment_services_using_teacher_id(id: UUID, db: Session= Depends(get_db), username: str= Depends(verify_teacher)):
    return delete_assignment_services_byTeacher(id, db, username)

@assignment_router.get("/assignment-services/{id}")
def get_assignment_service_using_id(id:UUID, db: Session= Depends(get_db), username: str=Depends(verify_user)):
    return fetch_assignment_service_using_id(id, db, username)

@assignment_router.post("/assignment-services/{id}/subscribe")
def subscribe_assignment_service(id:UUID, db: Session=Depends(get_db), username: str=Depends(verify_student)):
    return subscribe_assignmentService(id, db, username)

@assignment_router.get("/assignment-services/{id}/students")
def fetch_students_subscribedTo_service(id:UUID, db: Session=Depends(get_db), username: str=Depends(verify_user)):
    return fetch_students_subscribedTo_a_service(id, db, username)

@assignment_router.get("/students/{id}/assignment-services")
def fetch_services_subscribedBy_student(id: UUID, db:Session=Depends(get_db), username: str= Depends(verify_user)):
    return fetch_assignment_service_subcribedBy_a_student(id, db, username)

@assignment_router.get("/services/{id}/assignments")
def fetch_assignments_by_service_id(id: UUID, db: Session = Depends(get_db), username: str = Depends(verify_user)):
    """
    Fetch assignments by service ID.
    Requires user authentication.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    assignments = db.query(Assignment).filter(Assignment.assignment_service_id == id).all()

    if not assignments:
        raise  HTTPException(status_code=404, detail=f"not found any assignments for service {id}")

    return {"assignments":  assignments}

@assignment_router.get("/assignments/{id}")
def fetch_assignments_by_id(id:UUID, db:Session= Depends(get_db), username: str = Depends(verify_user)):
    return get_assignment_by_id(id,db,username)

@assignment_router.get("/assignment-service/assignment/{id}/questions")
def fetch_questions(id:UUID, db:Session = Depends(get_db), username: str = Depends(verify_user)):
    return get_questions_from_assignment(id, db, username)

@assignment_router.get("/assignment-services/assignment/question/{id}")
def fetch_question_using_id(id:UUID, db: Session=Depends(get_db), username: str = Depends(verify_user)):
    return get_questions_using_id(id, db, username)

@assignment_router.get("/assignment-service/assignment/question/{id}/answer")
def fetch_answers(id: UUID, db: Session=Depends(get_db), username: str= Depends(verify_user)):
    return get_answers_of_question(id, db, username)

@assignment_router.get("/assignment-service/assignment/question/answer/{id}")
def fetch_answer_using_id(id: UUID, db: Session=Depends(get_db), username: str= Depends(verify_user)):
    return get_answers_using_id(id, db, username)

@assignment_router.get("/students/{id1}/assignment-services/{id2}/assignment/{id3}/answers")
def fetch_answers_by_student(id1:UUID, id2:UUID, id3:UUID,db: Session=Depends(get_db), username: str =Depends(verify_teacher)):
    return get_answers_by_student(id1,id2, id3,db,username)

@assignment_router.get("/assignment-service/assignment/{id}/answers")
def fetch_answers_to_assignment(id: UUID, db: Session = Depends(get_db), username: str = Depends(verify_teacher)):
    return get_answers_to_assignment(id, db, username)

@assignment_router.get("/assignment-service/assignment/{id}/results")
def fetch_results_to_assignment(id:UUID, db:Session = Depends(get_db), username: str = Depends(verify_user)):
    return get_results_to_assignment(id,db,username)

@assignment_router.get("/results/{id}")
def fetch_results_by_id(id:UUID, db:Session= Depends(get_db), username: str = Depends(verify_user)):
    return get_results_by_id(id,db, username)
# -------------------------------------------------------------------------------------------STUDENT ROUTES------------------------------------------------------------------------------------------- 
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

@student_router.post("/assignment-service/assignment/question/{id}/answer")
def post_answers_to_question(id:UUID, answer: answer, db: Session= Depends(get_db), username: str = Depends(verify_student)):
    return post_answer(id,answer, db, username)

@student_router.get("/students/{id}/results")
def fetch_student_results(id:UUID, db: Session= Depends(get_db), username: str = Depends(verify_user)):
    return get_student_result(id, db, username)