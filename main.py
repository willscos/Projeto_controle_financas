from fastapi import FastAPI
from app.controllers.transacoes_controller import router as transacoes_router
from app.controllers.categorias_controller import router as categorias_router
from app.controllers.auth import router as auth_router
from app.models.database import init_db

app = FastAPI(title="API Controle Financeiro")

init_db()

app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
app.include_router(transacoes_router, prefix="/transacoes", tags=["Transações"])
app.include_router(categorias_router, prefix="/categorias", tags=["Categorias"])
