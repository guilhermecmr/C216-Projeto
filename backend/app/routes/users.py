from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("")
async def create(user: UserCreate):
    return await create_user(
        user.nome,
        user.email,
        user.senha
    )

@router.get("")
async def list_users():
    return await get_users()

@router.get("/{user_id}")
async def get_by_id(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário {user_id} não encontrado"
        )
    return user

@router.put("/{user_id}")
async def update(
    user_id: int,
    user: UserUpdate
):
    updated_user = await update_user(
        user_id,
        user.nome,
        user.email,
        user.senha
    )
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário {user_id} não encontrado"
        )
    return updated_user

@router.delete("/{user_id}")
async def delete(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário {user_id} não encontrado"
        )
    await delete_user(user_id)
    return {
        "message": f"Usuário {user_id} removido com sucesso"
    } 