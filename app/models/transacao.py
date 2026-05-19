from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.models.database import Base


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), nullable=False)  # receita ou despesa
    valor = Column(Float, nullable=False)
    categoria = Column(String(100), nullable=False)
    descricao = Column(String(255))
    data = Column(String(20), nullable=False)  # Changed from Date to String
    
    usuario_email = Column(
        String(150),
        ForeignKey("usuarios.email", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
