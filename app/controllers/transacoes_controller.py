from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.models.transacao import Transacao
from app.schemas.transacao_schema import TransacaoCreate, TransacaoResponse
from app.auth.deps import usuario_logado

# NO prefix - main.py handles this
router = APIRouter()


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


@router.get("/", response_model=List[TransacaoResponse])
def listar_transacoes(
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    return (
        db.query(Transacao)
        .filter(Transacao.usuario_email == usuario)
        .all()
    )


@router.get("/saldo")
def calcular_saldo(
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    transacoes = (
        db.query(Transacao)
        .filter(Transacao.usuario_email == usuario)
        .all()
    )

    saldo = sum(
        t.valor if t.tipo == "receita" else -t.valor
        for t in transacoes
    )

    return {"saldo": saldo}


@router.delete("/{id}")
def remover_transacao(
    id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    transacao = (
        db.query(Transacao)
        .filter(
            Transacao.id == id,
            Transacao.usuario_email == usuario
        )
        .first()
    )

    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    db.delete(transacao)
    db.commit()

    return {"mensagem": "Transação removida com sucesso"}
