from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class MemoryBase(BaseModel):
    url: HttpUrl
    title: str
    description: Optional[str] = None
    tags: Optional[list[str]] = []

class MemoryCreate(MemoryBase):
    pass

class Memory(MemoryBase):
    id: str
    user_id: str
    vector_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MemoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None