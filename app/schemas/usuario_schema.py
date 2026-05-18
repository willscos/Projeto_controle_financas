from pydantic import BaseModel


# ---------------------------
# BASE
# ---------------------------
class UsuarioBase(BaseModel):
    nome: str
    email: str


# ---------------------------
# CRIAÇÃO DE USUÁRIO
# ---------------------------
class UsuarioCreate(UsuarioBase):
    senha: str


# ---------------------------
# RESPOSTA DE USUÁRIO
# ---------------------------
class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True  # substitui orm_mode no Pydantic v2
