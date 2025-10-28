import streamlit as st
import sys
import os
from database import Database

db = Database()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from pages.cadastro import mostrar_tela_cadastro
from pages.relatorios import mostrar_tela_analises
from pages.analise_realocacao import mostrar_tela_custo_transporte
from components.sidebar import sidebar_menu
from pages.cadastrar_func_end import mostrar_tela_cadastro_enderecos

def mostrar_tela_principal():
    if "page" not in st.session_state:
        st.session_state["page"] = "usuario"

    if st.session_state["page"] == "logout":
        print("logout principal")
        st.session_state.clear()          
        st.session_state["pagina_atual"] = "login"
        st.rerun()                          

    sidebar_menu()                       

    if st.session_state["page"] == "usuario":
        mostrar_tela_cadastro()
    elif st.session_state["page"] == "analises":
        st.title("Tela de Análises")
    elif st.session_state["page"] == "transporte":
        mostrar_tela_custo_transporte()
    elif st.session_state["page"] == "funcionarios":
        mostrar_tela_cadastro_enderecos(db)