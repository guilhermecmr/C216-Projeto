from fastapi import APIRouter, HTTPException
from app.schemas.option import OptionCreate, OptionUpdate
from app.services.option_service import (
    create_option,
    get_options,
    get_option_by_id,
    get_options_by_poll,
    update_option,
    delete_option
)

router = APIRouter(
    prefix="/options",
    tags=["Options"]
)

@router.post("")
async def create(option: OptionCreate):
    return await create_option(
        option.texto,
        option.enquete_id
    )

@router.get("")
async def list_options():
    return await get_options()

@router.get("/poll/{poll_id}")
async def get_by_poll(poll_id: int):
    return await get_options_by_poll(poll_id)

@router.get("/{option_id}")
async def get_by_id(option_id: int):
    option = await get_option_by_id(option_id)
    if not option:
        raise HTTPException(
            status_code=404,
            detail="Opção {option_id} não encontrada"
        )
    return option

@router.put("/{option_id}")
async def update(
    option_id: int,
    option: OptionUpdate
):
    updated_option = await update_option(
        option_id,
        option.texto
    )
    if not updated_option:
        raise HTTPException(
            status_code=404,
            detail=f"Opção {option_id} não encontrada"
        )
    return updated_option

@router.delete("/{option_id}")
async def delete(option_id: int):
    option = await get_option_by_id(option_id)
    if not option:
        raise HTTPException(
            status_code=404,
            detail=f"Opção {option_id} não encontrada"
        )
    await delete_option(option_id)
    return {
        "message": f"Opção {option_id} removida com sucesso"
    }