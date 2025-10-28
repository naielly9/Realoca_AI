import streamlit as st
import os
import base64
from database import Database

db = Database()

def mostrar_logo():
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo", "logo_realoca_ai.png")
    logo_path = os.path.abspath(logo_path)
    if os.path.exists(logo_path):
        logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
        st.markdown(
            f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_base64}" width="120" style="margin-bottom:20px;"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning(f"Logo não encontrado no caminho: {logo_path}")

def mostrar_tela_login():
    st.markdown("""
    <style>

    .main-container {
        padding: 1rem 2rem;
    }
            
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-top: 5rem;
    }
    .login-title {
        text-align: center;
        color: #007bff;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .login-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .login-form {
        padding: 1rem 0;
    }
    .login-button {
        width: 100%;
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 1rem;
        cursor: pointer;
        margin-top: 1rem;
    }
    .login-button:hover {
        background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
        border: 1px solid #f5c6cb;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
        border: 1px solid #c3e6cb;
    }
    .info-box {
        background-color: #e3f2fd;
        color: #0277bd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #2196f3;
    }
    div[data-testid="stForm"] {
                margin-top: 0px !important;
                padding-top: 0px !important;
            }
    
    .stForm {
                background-color: white;
                border: 1px solid #f0f0f0;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.05);
                border-radius: 10px;
                padding: 20px;
                width: 100%;
                max-width: 420px;
                position: relative;
                font-family: 'Poppins', sans-serif;
                margin: 0px auto;
                text-align: center;
            }
            
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    #mostrar_logo()
    st.markdown(f'<h1 class="login-title">RealocAI</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="login-subtitle">Sistema Inteligente para Otimização de Transporte Corporativo com Foco em Eficiência Operacional</p>', unsafe_allow_html=True)
 
    with st.form("login_form"):
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("Entrar", use_container_width=True): 
                user = db.validar_usuario(username, senha) 
                if user: 
                    st.session_state["usuario"] = {"id": user[0], "nome": user[1] or username} 
                    st.success(f"Bem-vindo, {st.session_state['usuario']['nome']}!") 
                    st.rerun() 
                else: st.error("Usuário ou senha inválidos") 
            
            if st.form_submit_button("Cadastre-se",use_container_width=True): 
                st.session_state["pagina_atual"] = "cadastro" 
                st.rerun()
        
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
