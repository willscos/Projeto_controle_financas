from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.schemas.login_schema import LoginSchema
from app.auth.security import (
    gerar_hash,
    verificar_senha,
    criar_access_token,
    criar_refresh_token
)

router = APIRouter(tags=["Autenticação"])


# ---------------------------
# REGISTRO DE USUÁRIO
# ---------------------------
@router.post("/registrar", response_model=UsuarioResponse)
def registrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=gerar_hash(dados.senha)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# ---------------------------
# LOGIN
# ---------------------------
@router.post("/login")
def login(dados: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token_acesso = criar_access_token({"sub": usuario.email})
    token_refresh = criar_refresh_token({"sub": usuario.email})

    return {
        "access_token": token_acesso,
        "refresh_token": token_refresh,
        "token_type": "bearer"
    }
