from pydantic import BaseModel
from typing import Optional


class TransacaoBase(BaseModel):
    tipo: str
    valor: float
    categoria: str
    descricao: Optional[str] = None
    data: str  # Changed from date to str


class TransacaoCreate(TransacaoBase):
    pass


class TransacaoResponse(TransacaoBase):
    id: int

    class Config:
        from_attributes = True  # Fixed: was orm_mode
