from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.models.transacao import Transacao
from app.schemas.transacao_schema import TransacaoCreate, TransacaoResponse
from app.auth.deps import usuario_logado

# Add redirect_slashes=False to prevent 307 redirect loop!
router = APIRouter(redirect_slashes=False)


# ---------------------------
# CRIAR TRANSAÇÃO
# ---------------------------
@router.post("/", response_model=TransacaoResponse)
def criar_transacao(
    dados: TransacaoCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    nova = Transacao(
        **dados.dict(),
        usuario_email=usuario
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


# ---------------------------
# LISTAR TRANSAÇÕES
# ---------------------------
@router.get("/", response_model=list[TransacaoResponse])
def listar_transacoes(
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    return (
        db.query(Transacao)
        .filter(Transacao.usuario_email == usuario)
        .all()
    )
