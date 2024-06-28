from fastapi import APIRouter, Depends
from services import memory_service, auth_service
from models.user import User
from models.memory import memory

router = APIRouter()

@router.post("/memories")
async def add_memory(memory: memory, current_user: User = Depends(auth_service.get_current_user)):
    return await memory_service.add_memory(current_user.id, memory)

@router.get("/memories")
async def get_memories(current_user: User = Depends(auth_service.get_current_user)):
    return await memory_service.get_memories(current_user.id)

@router.delete("/memories/{memory_id}")
async def delete_memory(memory_id: str, current_user: User = Depends(auth_service.get_current_user)):
    return await memory_service.delete_memory(current_user.id, memory_id)