from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.models.database import Base

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # receita ou despesa
    valor = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    descricao = Column(String)
    data = Column(Date, nullable=False)

    # Transação pertence a um usuário
    usuario_email = Column(
        String,
        ForeignKey("usuarios.email", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
