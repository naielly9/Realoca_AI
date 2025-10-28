import streamlit as st

def criar_sessao(user):
    st.session_state["usuario"] = {"id": user[0], "nome": user[1]}

def check_session():
    return "usuario" in st.session_state

def logout_user():
    if "usuario" in st.session_state:
        del st.session_state["usuario"]
