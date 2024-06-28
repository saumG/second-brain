from http.client import HTTPException
from models.memory import memory
from database import cloudflare_d1
from services import vector_service
from integrations import github_integration, notion_integration, reddit_integration

async def add_memory(user_id: str, memory: memory):
    content = await extract_content(memory.url)
    vector = await vector_service.create_vector(content)
    vector_id = await vector_service.store_vector(vector)
    memory.vector_id = vector_id
    return await cloudflare_d1.insert_memory(user_id, memory)

async def memories(user_id: str):
    return await cloudflare_d1.memories(user_id)

async def delete_memory(user_id: str, memory_id: str):
    memory = await cloudflare_d1.get_memory(memory_id)
    if memory.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this memory")
    await vector_service.delete_vector(memory.vector_id)
    return await cloudflare_d1.delete_memory(memory_id)

async def extract_content(url: str):
    if "github.com" in url:
        return await github_integration.fetch_repo_content(url)
    elif "notion.so" in url:
        return await notion_integration.fetch_page_content(url)
    elif "reddit.com" in url:
        return await reddit_integration.fetch_post_content(url)
    else:
        # Default web scraping logic for other URLs
        # Implement web scraping here
        pass