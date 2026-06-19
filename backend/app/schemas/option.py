from pydantic import BaseModel

class OptionCreate(BaseModel):
    texto: str
    enquete_id: int

class OptionUpdate(BaseModel):
    texto: str

class OptionResponse(BaseModel):
    id: int
    texto: str
    enquete_id: int