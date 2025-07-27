import os
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from conf.db import get_db
from sqlalchemy.orm import Session
from models.db_models import Student
from dotenv import load_dotenv 

security = HTTPBearer()
load_dotenv()

def verify_student(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGO')])
        username = payload.get("sub")
        print(username)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token payload"
            )
        
        if db.query(Student).filter(Student.username == username).first() is None:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student not found"
            )
        elif db.query(Student).filter(Student.username == username).first().role.lower() != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a student"
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
    
