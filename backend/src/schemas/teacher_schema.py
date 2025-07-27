from pydantic import BaseModel, EmailStr, Field

class TeacherCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str | None = None 
    mobile: str | None = None
    college: str
    email: EmailStr 
    password: str

class TeacherUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    mobile: str | None = None
    college: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(min_length=8, max_length=128, default=None)

class TeacherSignin(BaseModel):
    email: EmailStr
    password: str
