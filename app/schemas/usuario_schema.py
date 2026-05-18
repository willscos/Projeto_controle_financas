from pydantic import BaseModel, EmailStr


# ---------------------------
# CRIAÇÃO DE USUÁRIO
# ---------------------------
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


# ---------------------------
# RESPOSTA DE USUÁRIO
# ---------------------------
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    model_config = {
        "from_attributes": True  # substitui orm_mode no Pydantic v2
    }
