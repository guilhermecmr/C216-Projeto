from pydantic import BaseModel

class VoteCreate(BaseModel):
    usuario_id: int
    enquete_id: int
    opcao_id: int