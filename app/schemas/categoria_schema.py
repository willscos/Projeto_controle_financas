from pydantic import BaseModel


# ---------------------------
# BASE
# ---------------------------
class CategoriaBase(BaseModel):
    nome: str


# ---------------------------
# CRIAÇÃO
# ---------------------------
class CategoriaCreate(CategoriaBase):
    pass


# ---------------------------
# RESPOSTA
# ---------------------------
class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True  # substitui orm_mode no Pydantic v2
