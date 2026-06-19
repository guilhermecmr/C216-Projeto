from fastapi import APIRouter, HTTPException
from app.schemas.poll import PollCreate, PollUpdate
from app.services.poll_service import create_poll, get_polls, get_poll_results, get_poll_by_id, update_poll, delete_poll

router = APIRouter(
    prefix="/polls",
    tags=["Polls"]
)

@router.post("")
async def create(poll: PollCreate):
    return await create_poll(
        poll.titulo,
        poll.descricao,
        poll.usuario_id
    )

@router.get("")
async def list_polls():
    return await get_polls()

@router.get("/results/{poll_id}")
async def results(poll_id: int):
    results = await get_poll_results(poll_id)
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Enquete {poll_id} não encontrada"
        )
    return results

@router.get("/{poll_id}")
async def get_by_id(poll_id: int):
    poll = await get_poll_by_id(poll_id)
    if not poll:
        raise HTTPException(
            status_code=404,
            detail=f"Enquete {poll_id} não encontrada"
        )
    return poll

@router.put("/{poll_id}")
async def update(
    poll_id: int,
    poll: PollUpdate
):
    updated_poll = await update_poll(
        poll_id,
        poll.titulo,
        poll.descricao
    )
    if not updated_poll:
        raise HTTPException(
            status_code=404,
            detail=f"Enquete {poll_id} não encontrada"
        )
    return updated_poll

@router.delete("/{poll_id}")
async def delete(poll_id: int):
    poll = await get_poll_by_id(poll_id)
    if not poll:
        raise HTTPException(
            status_code=404,
            detail=f"Enquete {poll_id} não encontrada"
        )
    await delete_poll(poll_id)
    return {
        "message": f"Enquete {poll_id} removida com sucesso"
    }