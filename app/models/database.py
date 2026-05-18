import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não encontrada nas variáveis de ambiente")

# Neon já inclui sslmode=require na URL → NÃO usar connect_args
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
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
    from app.models.transacao import Transacao
    from app.models.categoria import Categoria
    from app.models.usuario import Usuario
    from app.models.auditoria import Auditoria
    Base.metadata.create_all(bind=engine)
