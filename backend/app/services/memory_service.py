from fastapi import HTTPException
from fastapi.utils import generate_unique_id
from models.memory import MemoryCreate, Memory
from database import cloudflare_d1
from services import vector_service
from integrations import github, notion, reddit
from datetime import datetime

async def add_memory(user_id: str, memory: MemoryCreate):
    content = await extract_content(memory.url)
    vector = await vector_service.create_vector(content)
    vector_id = await vector_service.store_vector(vector)
    
    new_memory = Memory(
        id=generate_unique_id(), 
        user_id=user_id,
        vector_id=vector_id,
        created_at=datetime.now(datetime.UTC),
        updated_at=datetime.now(datetime.UTC)
    )
    
    return await cloudflare_d1.insert_memory(new_memory)

async def get_memories(user_id: str):
    return await cloudflare_d1.get_memories(user_id)

async def delete_memory(user_id: str, memory_id: str):
    memory = await cloudflare_d1.get_memory(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    if memory.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this memory")
    await vector_service.delete_vector(memory.vector_id)
    return await cloudflare_d1.delete_memory(memory_id)

async def extract_content(url: str):
    if "github.com" in url:
        return await github.fetch_repo_content(url)
    elif "notion.so" in url:
        return await notion.fetch_page_content(url)
    elif "reddit.com" in url:
        return await reddit.fetch_post_content(url)
    else:
        # Default web scraping logic for other URLs
        # Implement web scraping here
        pass