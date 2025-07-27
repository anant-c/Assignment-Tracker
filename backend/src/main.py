from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from conf.db import get_db
from routes.user_routes import signup_router, signin_router, student_router, teacher_router
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signup_router, prefix="/signup")
app.include_router(signin_router, prefix="/login")
# students
app.include_router(student_router, prefix="/fetch-teachers")
app.include_router(student_router, prefix="/students")
# teachers
app.include_router(teacher_router, prefix="/teachers")
app.include_router(teacher_router, prefix="/fetch-students")
app.include_router(teacher_router, prefix="/create-service")