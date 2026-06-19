from pydantic import BaseModel

class PollCreate(BaseModel):
    titulo: str
    descricao: str | None = None
    usuario_id: int

class PollUpdate(BaseModel):
    titulo: str
    descricao: str | None = None

class PollResponse(BaseModel):
    id: int
    titulo: str
    descricao: str | None
    usuario_id: int