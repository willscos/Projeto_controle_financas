from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria_schema import CategoriaCreate, CategoriaResponse
from app.auth.deps import usuario_logado

router = APIRouter()

@router.post("/", response_model=CategoriaResponse)
def criar_categoria(
    dados: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    nova = Categoria(**dados.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    return db.query(Categoria).all()
