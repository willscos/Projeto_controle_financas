import streamlit as st
import requests

# URL da sua API FastAPI no Render
API_URL = "https://projetocontrolefinancas-wsc.onrender.com"

st.set_page_config(page_title="Controle Financeiro", layout="wide")

st.title("💰 Controle Financeiro – Frontend Streamlit")


# ---------------------------
# FUNÇÃO DE LOGIN
# ---------------------------
def login(email, senha):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": email, "senha": senha},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"erro": str(e)}


# ---------------------------
# FUNÇÃO PARA BUSCAR TRANSAÇÕES
# ---------------------------
def get_transacoes(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/transacoes", headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {"erro": str(e)}


# ---------------------------
# INTERFACE DE LOGIN
# ---------------------------
if "token" not in st.session_state:
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        resultado = login(email, senha)

        if "access_token" in resultado:
            st.session_state["token"] = resultado["access_token"]
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Erro ao fazer login. Verifique suas credenciais.")
else:
    st.success("Você está logado!")

    # ---------------------------
    # LISTAR TRANSAÇÕES
    # ---------------------------
    st.subheader("📄 Suas Transações")

    dados = get_transacoes(st.session_state["token"])

    if isinstance(dados, list):
        st.dataframe(dados)
    else:
        st.error("Erro ao carregar transações")

    # ---------------------------
    # BOTÃO DE LOGOUT
    # ---------------------------
    if st.button("Sair"):
        del st.session_state["token"]
        st.rerun()
