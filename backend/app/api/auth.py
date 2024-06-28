from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from services import auth_service
from models.user import User

router = APIRouter()

@router.post("/register")
async def register(user: User):
    return await auth_service.register_user(user)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.login_user(form_data.username, form_data.password)

@router.get("/users/me")
async def get_current_user(current_user: User = Depends(auth_service.get_current_user)):
    return current_user