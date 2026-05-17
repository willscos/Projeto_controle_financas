from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import jwt, JWTError

from app.auth.security import SECRET_KEY, ALGORITHM
from app.models.database import SessionLocal
from app.models.auditoria import Auditoria


class AuditoriaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()

        usuario_email = "anônimo"

        # Tenta extrair o token manualmente (middleware não usa Depends)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                email = payload.get("sub")
                if email:
                    usuario_email = email
            except JWTError:
                pass  # token inválido → continua como "anônimo"

        # Continua a requisição
        response = await call_next(request)

        # Registra auditoria
        try:
            log = Auditoria(
                metodo=request.method,
                rota=request.url.path,
                usuario=usuario_email
            )
            db.add(log)
            db.commit()
        except:
            db.rollback()
        finally:
            db.close()

        return response
