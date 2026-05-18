from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.auth.security import decodificar_token
from app.models.database import SessionLocal
from app.models.auditoria import Auditoria


class AuditoriaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()

        usuario_email = "anônimo"

        # Extrai token manualmente (middleware não usa Depends)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            payload = decodificar_token(token)
            if payload and payload.get("sub"):
                usuario_email = payload["sub"]

        # Executa a requisição
        response = await call_next(request)

        # Registra auditoria
        try:
            log = Auditoria(
                metodo=request.method,
                rota=request.url.path,
                usuario=usuario_email,
                status=response.status_code,
                ip=request.client.host
            )
            db.add(log)
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

        return response
