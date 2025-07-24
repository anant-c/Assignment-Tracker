from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from conf.db import get_db
from routes.user_routes import router


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/signup")
app.include_router(router, prefix="/login")
# app.include_router(router, prefix="/teachers")
# app.include_router(router, prefix="/students")
# app.include_router(router, prefix="/assignment_services")
# app.include_router(router, prefix="/assignments")
# app.include_router(router, prefix="/questions")
# app.include_router(router, prefix="/answers")
# app.include_router(router, prefix="/results")



