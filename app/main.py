from fastapi import FastAPI
from app.controllers.auth import router as auth_router
from app.controllers.transacoes_controller import router as transacoes_router
from app.controllers.categorias_controller import router as categorias_router
from app.models.database import init_db
from app.middleware.auditoria import AuditoriaMiddleware




app = FastAPI(title="API Controle Financeiro")

init_db()

app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
app.include_router(transacoes_router, prefix="/transacoes", tags=["Transações"])
app.include_router(categorias_router, prefix="/categorias", tags=["Categorias"])
app.add_middleware(AuditoriaMiddleware)