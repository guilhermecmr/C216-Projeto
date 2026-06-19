from fastapi import APIRouter, HTTPException
from app.schemas.vote import VoteCreate
from app.services.vote_service import (
    user_exists,
    poll_exists,
    option_exists,
    option_belongs_to_poll,
    user_already_voted,
    register_vote
)

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("")
async def vote(vote: VoteCreate):
    if not await user_exists(vote.usuario_id):
        raise HTTPException(
            status_code=404,
            detail=f"Usuário {vote.usuario_id} não encontrado"
        )
    if not await poll_exists(vote.enquete_id):
        raise HTTPException(
            status_code=404,
            detail=f"Enquete {vote.enquete_id} não encontrada"
        )
    if not await option_exists(vote.opcao_id):
        raise HTTPException(
            status_code=404,
            detail=f"Opção {vote.opcao_id} não encontrada"
        )
    if not await option_belongs_to_poll(
        vote.opcao_id,
        vote.enquete_id
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Opção {vote.opcao_id} não pertence à enquete {vote.enquete_id}"
        )
    if await user_already_voted(
        vote.usuario_id,
        vote.enquete_id
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Usuário {vote.usuario_id} já votou nesta enquete"
        )
    return await register_vote(
        vote.usuario_id,
        vote.enquete_id,
        vote.opcao_id
    )