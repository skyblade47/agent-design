"""
todos API Endpoint
"""
from fastapi import APIRouter

router = APIRouter(prefix="/todos")

@router.get("/")
async def get_todos():
    return {"message": "todos endpoint working"}
