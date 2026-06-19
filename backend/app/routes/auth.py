from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest
from app.services.auth_service import login

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
async def user_login(data: LoginRequest):

    user = await login(
        data.email,
        data.senha
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )
    return user