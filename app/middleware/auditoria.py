from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from app.auth.deps import tentar_pegar_usuario  # versão que não explode se não tiver token

class AuditoriaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        usuario = await tentar_pegar_usuario(request)
        resposta = await call_next(request)

        # aqui você pode salvar em banco:
        # rota, método, usuário, status, data/hora
        print(f"[AUDITORIA] {datetime.utcnow()} - {request.method} {request.url.path} - {usuario} - {resposta.status_code}")

        return resposta
