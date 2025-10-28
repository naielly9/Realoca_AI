import streamlit as st
from database import Database

db = Database()

def mostrar_tela_cadastro():
    st.title("📝 Cadastro de Usuário")

    nome = st.text_input("Nome completo")
    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar", use_container_width=True):
        if not username or not senha:
            st.warning("Preencha todos os campos obrigatórios!")
        else:
            sucesso = db.cadastrar_usuario(username, senha, nome)
            if sucesso:
                st.success("Usuário cadastrado com sucesso! Faça login.")
                st.session_state["pagina_atual"] = "login"
                st.rerun()
            else:
                st.error("Usuário já existente. Escolha outro nome de usuário.")

    if st.button("Voltar para login"):
        st.session_state["pagina_atual"] = "login"
        st.rerun()
