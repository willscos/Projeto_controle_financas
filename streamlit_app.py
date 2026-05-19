import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date

# URL da API FastAPI no Render
API_URL = "https://projeto-controle-financas.onrender.com"

st.set_page_config(page_title="Controle Financeiro", layout="wide")

st.title("💰 Controle Financeiro – Dashboard Completo")


# ============================
# FUNÇÕES DE API
# ============================

def login(email, senha):
    try:
        r = requests.post(f"{API_URL}/auth/login", json={"email": email, "senha": senha})
        return r.json()
    except:
        return {"erro": "Erro ao conectar com o servidor"}


def registrar_usuario(nome, email, senha):
    try:
        r = requests.post(
            f"{API_URL}/auth/registrar",
            json={"nome": nome, "email": email, "senha": senha}
        )
        return r.json()
    except:
        return {"erro": "Erro ao conectar com o servidor"}


def get_transacoes(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{API_URL}/transacoes/", headers=headers)
    try:
        return r.json()
    except:
        return []


def criar_transacao(token, dados):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{API_URL}/transacoes/", json=dados, headers=headers)
    return r.json()


# ✅ NOVA: Atualizar transação
def atualizar_transacao(token, id, dados):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.put(f"{API_URL}/transacoes/{id}", json=dados, headers=headers)
    return r.json()


# ✅ NOVA: Deletar transação
def remover_transacao(token, id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{API_URL}/transacoes/{id}", headers=headers)
    return r.json()


# ============================
# MENU INICIAL (LOGIN / CADASTRO)
# ============================

if "token" not in st.session_state:

    menu_login = st.radio("Acesso", ["Entrar", "Criar Conta"])

    if menu_login == "Entrar":
        st.subheader("🔐 Login")

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            resultado = login(email, senha)

            if "access_token" in resultado:
                st.session_state["token"] = resultado["access_token"]
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Credenciais inválidas ou erro no servidor.")

    else:
        st.subheader("🧑‍💻 Criar Conta")

        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        confirmar = st.text_input("Confirmar senha", type="password")

        if st.button("Registrar"):
            if senha != confirmar:
                st.error("As senhas não coincidem.")
            else:
                resultado = registrar_usuario(nome, email, senha)

                if "id" in resultado:
                    st.success("✅ Conta criada com sucesso! Agora faça login.")
                else:
                    st.error(resultado.get("detail", "Erro ao registrar usuário."))

else:
    st.success("✅ Você está logado!")

    token = st.session_state["token"]

    # ============================
    # MENU LATERAL
    # ============================
    menu = st.sidebar.radio(
        "Menu", 
        ["📊 Dashboard", "📄 Transações", "➕ Nova Transação", "✏️ Editar_transação", "🚪 Sair"]
    )

    # ============================
    # DASHBOARD
    # ============================
    if menu == "📊 Dashboard":
        st.subheader("📊 Dashboard Financeiro")

        dados = get_transacoes(token)

        if isinstance(dados, list) and len(dados) > 0:
            df = pd.DataFrame(dados)

            col1, col2, col3 = st.columns(3)

            with col1:
                total_receitas = df[df["tipo"] == "receita"]["valor"].sum()
                st.metric("Total de Receitas", f"R$ {total_receitas:,.2f}")

            with col2:
                total_despesas = df[df["tipo"] == "despesa"]["valor"].sum()
                st.metric("Total de Despesas", f"R$ {total_despesas:,.2f}")

            with col3:
                saldo = total_receitas - total_despesas
                st.metric("Saldo", f"R$ {saldo:,.2f}")

            fig = px.pie(df, names="categoria", values="valor", title="Distribuição por Categoria")
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Nenhuma transação encontrada.")

    # ============================
    # LISTAGEM DE TRANSAÇÕES
    # ============================
    if menu == "📄 Transações":
        st.subheader("📄 Suas Transações")

        dados = get_transacoes(token)

        if isinstance(dados, list) and len(dados) > 0:
            # Formata para exibição bonita
            df = pd.DataFrame(dados)
            df = df.sort_values("data", ascending=False)
            
            # Renomeia colunas para português
            df_display = df.rename(columns={
                "id": "ID",
                "tipo": "Tipo",
                "valor": "Valor",
                "categoria": "Categoria",
                "descricao": "Descrição",
                "data": "Data",
                "usuario_email": "Usuário"
            })
            
            st.dataframe(df_display, use_container_width=True)
            
            st.info(f"Total: {len(dados)} transações")
        elif isinstance(dados, list) and len(dados) == 0:
            st.info("Nenhuma transação encontrada.")
        else:
            st.error("Erro ao carregar transações")

    # ============================
    # CRIAR NOVA TRANSAÇÃO
    # ============================
    if menu == "➕ Nova Transação":
        st.subheader("➕ Nova Transação")

        tipo = st.selectbox("Tipo", ["receita", "despesa"])
        valor = st.number_input("Valor", min_value=0.01, step=0.01)
        categoria = st.text_input("Categoria")
        descricao = st.text_input("Descrição")
        
        data_selecionada = st.date_input("Data")
        data_formatada = data_selecionada.strftime("%Y-%m-%d")

        if st.button("💾 Salvar"):
            dados = {
                "tipo": tipo,
                "valor": valor,
                "categoria": categoria,
                "descricao": descricao,
                "data": data_formatada
            }

            resultado = criar_transacao(token, dados)

            if "id" in resultado:
                st.success("✅ Transação criada com sucesso!")
            else:
                st.error(resultado.get("detail", "Erro ao criar transação."))

    # ============================
    # ✏️ EDITAR / DELETAR TRANSAÇÃO
    # ============================
    if menu == "✏️ Editar_transação":
        st.subheader("✏️ Editar ou Remover Transação")
        
        dados = get_transacoes(token)
        
        if isinstance(dados, list) and len(dados) > 0:
            # Cria opção de seleção
            opcoes = {f"ID {t['id']} - {t['tipo']} - R$ {t['valor']} - {t['categoria']}": t['id'] for t in dados}
            opcoes["Selecione..."] = 0
            
            selecionado = st.selectbox(
                "Selecione a transação:",
                options=list(opcoes.keys()),
                index=0
            )
            
            if selecionado != "Selecione...":
                transacao_id = opcoes[selecionado]
                transacao = next((t for t in dados if t["id"] == transacao_id), None)
                
                if transacao:
                    st.divider()
                    
                    # Campos para editar
                    novo_tipo = st.selectbox(
                        "Tipo", 
                        ["receita", "despesa"], 
                        index=0 if transacao["tipo"] == "receita" else 1
                    )
                    novo_valor = st.number_input(
                        "Valor", 
                        min_value=0.01, 
                        step=0.01,
                        value=float(transacao["valor"])
                    )
                    nova_categoria = st.text_input(
                        "Categoria", 
                        value=transacao["categoria"]
                    )
                    nova_descricao = st.text_input(
                        "Descrição", 
                        value=transacao.get("descricao", "") or ""
                    )
                    
                    # Converte data
                    data_original = transacao["data"]
                    try:
                        data_date = date.fromisoformat(data_original)
                    except:
                        data_date = date.today()
                    
                    nova_data = st.date_input("Data", value=data_date)
                    data_final = nova_data.strftime("%Y-%m-%d")
                    
                    st.divider()
                    
                    # Botões de ação
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("💾 Atualizar Transação", use_container_width=True):
                            dados_att = {
                                "tipo": novo_tipo,
                                "valor": novo_valor,
                                "categoria": nova_categoria,
                                "descricao": nova_descricao,
                                "data": data_final
                            }
                            
                            resultado = atualizar_transacao(token, transacao_id, dados_att)
                            
                            if "id" in resultado:
                                st.success("✅ Transação atualizada com sucesso!")
                            else:
                                st.error(f"Erro ao atualizar: {resultado.get('detail', 'Erro desconhecido')}")
                    
                    with col2:
                        if st.button("🗑️ Remover Transação", type="primary", use_container_width=True):
                            resultado = remover_transacao(token, transacao_id)
                            
                            if "mensagem" in resultado:
                                st.success("✅ Transação removida com sucesso!")
                                st.rerun()
                            else:
                                st.error(f"Erro ao remover: {resultado.get('detail', 'Erro desconhecido')}")
                
        else:
            st.info("Nenhuma transação para editar.")

    # ============================
    # LOGOUT
    # ============================
    if menu == "🚪 Sair":
        del st.session_state["token"]
        st.rerun()
