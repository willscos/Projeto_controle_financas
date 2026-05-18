from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.auth import router as auth_router
from app.controllers.transacoes_controller import router as transacoes_router
from app.controllers.categorias_controller import router as categorias_router
from app.models.database import init_db
from app.middleware.auditoria import AuditoriaMiddleware


app = FastAPI(title="API Controle Financeiro")

# Inicializa o banco (somente porque você não usa Alembic)
init_db()

# CORS (seguro e compatível com qualquer frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # qualquer origem
    allow_credentials=False,      # obrigatório quando allow_origins="*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de auditoria (vem depois do CORS)
app.add_middleware(AuditoriaMiddleware)

# Rotas
app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
app.include_router(transacoes_router, prefix="/transacoes", tags=["Transações"])
app.include_router(categorias_router, prefix="/categorias", tags=["Categorias"])

# Rota raiz (Render usa isso para health check)
@app.get("/")
def root():
    return {"status": "ok", "mensagem": "API rodando!"}
