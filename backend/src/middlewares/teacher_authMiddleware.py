import os
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from conf.db import get_db
from sqlalchemy.orm import Session
from models.db_models import Teacher
from dotenv import load_dotenv 

security = HTTPBearer()
load_dotenv()

def verify_teacher(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGO')])
        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token payload"
            )

        if db.query(Teacher).filter(Teacher.username == username).first() is None:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teacher not found"
            )
        elif db.query(Teacher).filter(Teacher.username == username).first().role.lower() != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a teacher"
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
    
