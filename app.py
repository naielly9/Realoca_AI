import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from pages.login import mostrar_tela_login
from pages.cadastro import mostrar_tela_cadastro
from pages.principal import mostrar_tela_principal
from utils.style import carregar_custom_css_do_tema

tema = "tema-azul"
custom_css = carregar_custom_css_do_tema("styles.css", tema)
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

def load_css(file_name):
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            st.warning("Arquivo de estilo não encontrado. Verifique o caminho do styles.css.")
    
load_css("styles.css")
def esconder_sidebar():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Realoca_AI", layout="wide")

if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "login"

if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

pagina_atual = st.session_state.get("pagina_atual", "login")

if st.session_state["usuario"]:
    mostrar_tela_principal()  
elif pagina_atual == "cadastro":
    mostrar_tela_cadastro()
else:
    esconder_sidebar()
    mostrar_tela_login()
