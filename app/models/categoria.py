from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # Categoria pertence a um usuário
    usuario_email = Column(
        String,
        ForeignKey("usuarios.email", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
