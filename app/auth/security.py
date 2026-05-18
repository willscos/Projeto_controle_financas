from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

# ---------------------------
# CONFIGURAÇÕES
# ---------------------------

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Validação obrigatória em produção
if not SECRET_KEY:
    raise ValueError("⚠️ A variável de ambiente SECRET_KEY não está definida!")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------
# HASH DE SENHA
# ---------------------------

def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash_senha: str):
    return pwd_context.verify(senha, hash_senha)


# ---------------------------
# CRIAÇÃO DE TOKENS
# ---------------------------

def criar_access_token(dados: dict):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def criar_refresh_token(dados: dict):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------
# DECODIFICAÇÃO DE TOKEN
# ---------------------------

def decodificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
