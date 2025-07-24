from fastapi import APIRouter
from controllers.teacher_controller import get_teachers

router = APIRouter()

@router.post("/")
async def get_users():
    return await get_teachers()