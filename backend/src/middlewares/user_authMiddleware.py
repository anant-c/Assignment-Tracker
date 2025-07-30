import os
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from conf.db import get_db
from sqlalchemy.orm import Session
from models.db_models import Teacher, Student
from dotenv import load_dotenv 

security = HTTPBearer()
load_dotenv()
# Middleware to verify user authentication no role matter teacher or student

def verify_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGO')])
        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token payload"
            )

        teacher = db.query(Teacher).filter(Teacher.username == username).first()
        student = db.query(Student).filter(Student.username == username).first()
        if teacher is None and student is None:
        
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found"
            )
    
        
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please sign in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token."
        )
    
