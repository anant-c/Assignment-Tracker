import os
from sqlalchemy.orm import Session
from models.db_models import Teacher, AssignmentService, Assignment, Question, Result
from fastapi import HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from schemas.teacher_schema import TeacherCreate, TeacherUpdate, TeacherSignin
from schemas.assignment_schema import update_assignment_service, assignment, assignment_update, question, question_update, result, resultUpdate
import jwt
from uuid import UUID 

def create_teacher(db: Session, teacher: TeacherCreate):
    if(not teacher.username or not teacher.first_name or not teacher.last_name or not teacher.role or not teacher.college or not teacher.email or not teacher.password):
        raise ValueError("All fields are required")

    if(db.query(Teacher).filter(Teacher.username == teacher.username.strip()).first()):
        raise ValueError("Username already exists")

    if(db.query(Teacher).filter(Teacher.email == teacher.email.strip()).first()):
        raise ValueError("Email already exists")
    
    # Hash the password
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = password_context.hash(teacher.password)

    new_teacher = Teacher(
        username=teacher.username,
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        role=teacher.role,
        mobile=teacher.mobile,
        college=teacher.college,
        email=teacher.email,
        password=hashed_password
    )
    token = jwt.encode({"sub": new_teacher.username}, os.getenv("JWT_SECRET_KEY"), algorithm= os.getenv("JWT_ALGO"))
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    
    return {"message": "Teacher created successfully", "token": token, "teacher_id": str(new_teacher.id)}


def signinTeacher(email: str, password: str, db: Session):
    if not email or not password:
        raise ValueError("Email and password are required")

    teacher = db.query(Teacher).filter(Teacher.email == email.strip()).first()
    if not teacher:
        raise ValueError("Invalid email or password")

    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not password_context.verify(password, teacher.password):
        raise ValueError("Invalid password")

    token = jwt.encode({"sub": teacher.username}, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGO"))
    
    return {"message": "Signin successful", "token": token, "teacher_id": str(teacher.id)}


def update_teacher_profile(id: UUID, updateTeacher: TeacherUpdate, db: Session, username: str):
    print(f"Authenticated teacher: {username}")

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Ensure the authenticated teacher can only update their own profile
    if(username != db.query(Teacher).filter(Teacher.id == id).first().username):
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")


    # Update only the fields that are provided in the request
    for key, value in updateTeacher.dict(exclude_unset=True).items():
        if value is not None:
            if key == "password":
                # Hash the password if it's being updated
                password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                value = password_context.hash(value)

            setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher

def create_assignment_service(name:str, description:str, teacher_id:UUID, db:Session, username:str):
    """
    Create a new assignment service.
    Requires teacher authentication.
    """
    print(f"Authenticated teacher: {username}")
    new_service = AssignmentService(
        name=name,
        description=description,
        teacher_id=teacher_id
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)


    return {"message": f"Assignment service {new_service.id} created successfully by", "teacher: ": username}

def update_assigment_service(id:UUID, update_service: update_assignment_service,  db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    service = db.query(AssignmentService).filter(AssignmentService.id == id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found.")
    
    teacher = db.query(Teacher).filter(Teacher.id == service.teacher_id).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found corresponding to the service.")
    
    if teacher.username != username:
        print(teacher.username, username)
        raise HTTPException(status_code=401, detail="You are not authorized to update this service.")
    
    # update only the fields which are available
    for key, value in update_service.dict(exclude_unset=True).items():
        if value is not None:
            setattr(service, key, value)

    db.commit()
    db.refresh(service)
    return service

def delete_assignment_services_byTeacher(id: UUID, db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    service = db.query(AssignmentService).filter(AssignmentService.id == id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found.")


    teacher = db.query(Teacher).filter(Teacher.id == service.teacher_id).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found corresponding to the service.")
    
    if teacher.username != username:
        print(teacher.username, username)
        raise HTTPException(status_code=401, detail="You are not authorized to delete this service.")


    db.delete(service)
    db.commit()

    return {"message": "Service deleted successfully."}

def post_assignments(id: UUID, assignment: assignment, db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    service = db.query(AssignmentService).filter(AssignmentService.id == id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Assignment Service not found, so cann't post assignment.")
    
    teacher_id = service.teacher_id

    owner_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not owner_teacher:
        raise HTTPException(status_code=404, detail="The teacher who created this service is not found.")
    
    if owner_teacher.username != username:
        raise HTTPException(status_code=401, detail="You are not authorized to post assignments on this service.")
    
    newassignment = Assignment(
        title=assignment.title,
        description = assignment.description,
        due_date = assignment.due_date,
        status= assignment.status,
        assignment_service_id = id
    )

    db.add(newassignment)
    db.commit()
    db.refresh(newassignment)

    return {
        "message": f"Assignment added by {owner_teacher.first_name} in {service.name} assignment service."
    }

def update_assignment(id: UUID, assignment_update: assignment_update, db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    service_id = assignment.assignment_service_id

    service = db.query(AssignmentService).filter(AssignmentService.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Parent Service not found.")
    
    owner = db.query(Teacher).filter(service.teacher_id == Teacher.id).first()

    if not owner:
        raise HTTPException(status_code=404, detail="Teacher who owns this service not found.")
    
    if owner.username != username:
        raise HTTPException(status_code=401, detail="You don't have access to this assignment service.")

    for key, value in assignment_update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(assignment, key, value)

    db.commit()
    db.refresh(assignment)

    return assignment

def delete_assignment(id: UUID, db: Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    service_id = assignment.assignment_service_id

    service = db.query(AssignmentService).filter(AssignmentService.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Parent Service not found.")
    
    owner = db.query(Teacher).filter(service.teacher_id == Teacher.id).first()

    if not owner:
        raise HTTPException(status_code=404, detail="Teacher who owns this service not found.")
    
    if owner.username != username:
        raise HTTPException(status_code=401, detail="You don't have access to this assignment service.")
    
    db.delete(assignment)
    db.commit()

    return {"message": f"Deleted {assignment.id} successfully."}

def post_questions(id: UUID, question:question, db: Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    ques = Question(
        text= question.text,
        assignment_id= id
    )

    assignment = db.query(Assignment).filter(Assignment.id == id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found to post question.")
    
    service_id = assignment.assignment_service_id

    service = db.query(AssignmentService).filter(AssignmentService.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Assignment Service not found for the assignment to post questions.")
    
    teacher_id = service.teacher_id

    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher who owns this Assignment Service not found.")

    if teacher.username != username:
        raise HTTPException(status_code=401, detail="You are not allowed to post questions in this assignment, assignment-service owner is different.")
    
    db.add(ques)
    db.commit()
    db.refresh(ques)

    return {
        "message": f"Question posted by {teacher.first_name} in assignment: {assignment.title}",
        "question": ques
    }

def update_question(id:UUID, edit_question: question_update, db:Session, username:str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    question = db.query(Question).filter(Question.id == id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    
    assignment_id = question.assignment_id

    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    service_id = assignment.assignment_service_id

    service = db.query(AssignmentService).filter(AssignmentService.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Parent Service not found.")
    
    owner = db.query(Teacher).filter(service.teacher_id == Teacher.id).first()

    if not owner:
        raise HTTPException(status_code=404, detail="Teacher who owns the assignment service for this question was not found.")
    
    if owner.username != username:
        raise HTTPException(status_code=401, detail="You don't have access to this assignment service.")
    
    for key, value in edit_question.dict(exclude_unset=True).items():
        if value is not None:
            setattr(question, key, value)

    db.commit()
    db.refresh(question)

    return {
        "message": "Question updated successfully.",
        "question": question
    }

def delete_question(id:UUID, db: Session, username: str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    question = db.query(Question).filter(Question.id == id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    
    assignment_id = question.assignment_id

    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    service_id = assignment.assignment_service_id

    service = db.query(AssignmentService).filter(AssignmentService.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Parent Service not found.")
    
    owner = db.query(Teacher).filter(service.teacher_id == Teacher.id).first()

    if not owner:
        raise HTTPException(status_code=404, detail="Teacher who owns the assignment service for this question was not found.")
    
    if owner.username != username:
        raise HTTPException(status_code=401, detail="You don't have access to this assignment service.")
    
    db.delete(question)
    db.commit()

    return{
        "message": f"Question with id: {id} deleted successfully."
    }

def create_result(id1:UUID, id2:UUID,result:result ,db:Session, username: str):

    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    assignment = db.query(Assignment).filter(Assignment.id == id1).first()

    if not assignment:
        raise HTTPException(status_code=404, detail=f"Assignment with id: {id1} not found to post the result.")
    
    assignment_service_id = assignment.assignment_service_id
    assignment_service = db.query(AssignmentService).filter(AssignmentService.id == assignment_service_id).first()

    if not assignment_service:
        raise HTTPException(status_code=404, detail=f"Assignment Service for this result is not found, so cann't post result.")
    
    teacher_id = assignment_service.teacher_id
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail=f"Owner teacher for this assignment with username {teacher.username} is not found, so cann't post the result.")
    
    if username != teacher.username:
        raise HTTPException(status_code=401, detail="Unauthorized access, you cann't post result for this assignment.")
    
    new_result = Result(
        student_id= id2,
        assignment_id= id1,
        score = result.score,
        feedback= result.feedback
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return{
        "message": f"Result for student with id:{id2} for assignment with title: {assignment.title} is published.",
        "result": new_result
    }

def update_result(id:UUID, resultUpdate:resultUpdate, db:Session, username:str):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = db.query(Result).filter(Result.id == id).first()

    if not result:
        raise HTTPException(status_code=401, detail="Result not found to update.")
    
    assignment_id = result.assignment_id
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment no found.")
    
    assignment_service_id = assignment.assignment_service_id
    assignment_service = db.query(AssignmentService).filter(AssignmentService.id == assignment_service_id).first()

    if not assignment_service:
        raise HTTPException(status_code=404, detail="Assignment Service not found.")
    
    teacher_id = assignment_service.teacher_id

    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found for this result to modify.")
    
    if teacher.username != username:
        raise HTTPException(status_code=401, detail=f"Unauthorized access only teacher with username: {teacher.username} can modify this result.")
    
    for key,value in resultUpdate.dict(exclude_unset=True).items():
        if value is not None:
            setattr(result, key, value)
    
    db.commit()
    db.refresh(result)

    return {
        "message": "Result updated successfully.",
        "result": result
    }
    