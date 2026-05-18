from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decodificar_token
from app.models.database import get_db
from app.models.usuario import Usuario

# O tokenUrl deve apontar para um endpoint que aceite OAuth2 (form-data)
# Como seu login usa JSON, deixamos apenas um placeholder funcional
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ---------------------------------------------------------
# 1. Retorna APENAS o email do usuário logado
# ---------------------------------------------------------
def usuario_logado(token: str = Depends(oauth2_scheme)):
    payload = decodificar_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")

    return email


# ---------------------------------------------------------
# 2. Retorna o OBJETO Usuario completo
# ---------------------------------------------------------
def get_usuario_logado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decodificar_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


# ---------------------------------------------------------
# 3. Verifica se o usuário é ADMIN
# ---------------------------------------------------------
def requer_admin(usuario: Usuario = Depends(get_usuario_logado)):
    # Seu modelo Usuario NÃO tem campo role
    # Então adicionamos uma proteção
    if not hasattr(usuario, "role"):
        raise HTTPException(status_code=500, detail="Campo 'role' não existe no modelo Usuario")

    if usuario.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão")

    return usuario
