from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware  # ADD THIS

from app.controllers.auth import router as auth_router
from app.controllers.transacoes_controller import router as transacoes_router
from app.controllers.categorias_controller import router as categorias_router
from app.models.database import init_db
from app.middleware.auditoria import AuditoriaMiddleware


app = FastAPI(title="API Controle Financeiro")

# REMOVE any HTTPS redirect middleware if it exists!
# app.add_middleware(HTTPSRedirectMiddleware) <- REMOVE THIS

# If HTTPSRedirectMiddleware exists in your middleware folder, disable it!

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuditoriaMiddleware)

app.include_router(auth_router, tags=["Autenticação"])
app.include_router(transacoes_router, tags=["Transações"])
app.include_router(categorias_router, tags=["Categorias"])

@app.get("/")
def root():
    return {"status": "ok", "mensagem": "API rodando!"}
