from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.transacao import Transacao
from app.schemas.transacao_schema import TransacaoCreate, TransacaoResponse
from app.auth.deps import usuario_logado

router = APIRouter()

@router.post("/", response_model=TransacaoResponse)
def criar_transacao(
    dados: TransacaoCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    nova = Transacao(**dados.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/", response_model=list[TransacaoResponse])
def listar_transacoes(
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    return db.query(Transacao).all()

@router.get("/saldo")
def calcular_saldo(
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    transacoes = db.query(Transacao).all()
    saldo = sum(t.valor if t.tipo == "receita" else -t.valor for t in transacoes)
    return {"saldo": saldo}

@router.delete("/{id}")
def remover_transacao(
    id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    db.query(Transacao).filter(Transacao.id == id).delete()
    db.commit()
    return {"mensagem": "Transação removida"}
