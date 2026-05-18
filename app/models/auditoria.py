from sqlalchemy import Column, Integer, String
from app.models.database import Base

class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    metodo = Column(String, nullable=False)
    rota = Column(String, nullable=False)
    usuario = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    ip = Column(String, nullable=False)
