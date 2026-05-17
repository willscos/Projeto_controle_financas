from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria_schema import CategoriaCreate, CategoriaResponse
from app.auth.deps import usuario_logado

router = APIRouter()


# ---------------------------
# CRIAR CATEGORIA
# ---------------------------
@router.post("/", response_model=CategoriaResponse)
def criar_categoria(
    dados: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    # Verifica se já existe categoria com o mesmo nome para este usuário
    existente = (
        db.query(Categoria)
        .filter(
            Categoria.nome == dados.nome,
            Categoria.usuario_email == usuario
        )
        .first()
    )

    if existente:
        raise HTTPException(status_code=400, detail="Categoria já existe")

    nova = Categoria(
        **dados.dict(),
        usuario_email=usuario  # associa ao usuário logado
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


# ---------------------------
# LISTAR CATEGORIAS DO USUÁRIO
# ---------------------------
@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    return (
        db.query(Categoria)
        .filter(Categoria.usuario_email == usuario)
        .all()
    )


# ---------------------------
# REMOVER CATEGORIA
# ---------------------------
@router.delete("/{id}")
def remover_categoria(
    id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    categoria = (
        db.query(Categoria)
        .filter(
            Categoria.id == id,
            Categoria.usuario_email == usuario
        )
        .first()
    )

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.delete(categoria)
    db.commit()

    return {"mensagem": "Categoria removida com sucesso"}
