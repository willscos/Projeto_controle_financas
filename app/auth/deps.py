from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.auth.security import SECRET_KEY, ALGORITHM
from app.models.database import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------------------------------------------------------
# 1. Retorna APENAS o email do usuário logado
# ---------------------------------------------------------
def usuario_logado(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ---------------------------------------------------------
# 2. Retorna o OBJETO Usuario completo (para permissões)
# ---------------------------------------------------------
def get_usuario_logado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


# ---------------------------------------------------------
# 3. Verifica se o usuário é ADMIN
# ---------------------------------------------------------
def requer_admin(usuario: Usuario = Depends(get_usuario_logado)):
    if usuario.role != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão")
    return usuario
