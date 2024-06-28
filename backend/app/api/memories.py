from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services import memory_service, auth_service
from models.user import User
from models.memory import MemoryCreate, Memory

router = APIRouter()

@router.post("/memories", response_model=Memory)
async def add_memory(memory: MemoryCreate, current_user: User = Depends(auth_service.get_current_user)):
    return await memory_service.add_memory(current_user.id, memory)

@router.get("/memories", response_model=List[Memory])
async def get_memories(current_user: User = Depends(auth_service.get_current_user)):
    return await memory_service.get_memories(current_user.id)

@router.delete("/memories/{memory_id}", response_model=dict)
async def delete_memory(memory_id: str, current_user: User = Depends(auth_service.get_current_user)):
    result = await memory_service.delete_memory(current_user.id, memory_id)
    if result:
        return {"message": "Memory deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Memory not found")