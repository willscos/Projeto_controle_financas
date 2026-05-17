import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não encontrada nas variáveis de ambiente")

# Neon exige SSL
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Importa os modelos para registrar no metadata
    from app.models.transacao import Transacao
    from app.models.categoria import Categoria
    from app.models.usuario import Usuario
    Base.metadata.create_all(bind=engine)
