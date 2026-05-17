from pydantic import BaseModel
from datetime import date

class TransacaoBase(BaseModel):
    tipo: str
    valor: float
    categoria: str
    descricao: str | None = None
    data: date

class TransacaoCreate(TransacaoBase):
    pass

class TransacaoResponse(TransacaoBase):
    id: int

    class Config:
        orm_mode = True
