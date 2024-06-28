from fastapi import FastAPI
from api import auth, memories, chat, settings
from database import cloudflare_d1, cloudflare_vector

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Initialize database connections
    await cloudflare_d1.init()
    await cloudflare_vector.init()

app.include_router(auth.router)
app.include_router(memories.router)
app.include_router(chat.router)
app.include_router(settings.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)