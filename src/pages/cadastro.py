import streamlit as st
from database import Database

db = Database()

def mostrar_tela_cadastro():
    st.markdown("""
    <style>
    .main-container {
        padding: 1rem 2rem;
    }

    .painel-header {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #e6e6e6;
        padding-bottom: 0.5rem;
    }

    .titulo-pagina {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.6rem;
        font-weight: 700;
        color: black;
    }

    .material-icons {
        font-size: 1.8rem;
        color: #004080;
    }

    .cadastro-container {
        max-width: 420px;
        margin: 0 auto;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        padding: 2rem;
        text-align: center;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        margin-top: 1rem;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
    }

    .voltar-btn > button {
        background: #f1f1f1;
        color: #333;
    }

    .voltar-btn > button:hover {
        background: #e1e1e1;
    }

    </style>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="painel-header">
        <div class="titulo-pagina">
            <span class="material-icons">person_add</span>
            <span>Cadastro de Usuário</span>
        </div>
    </div>
""", unsafe_allow_html=True)
  

    with st.form("cadastro_form"):
        nome = st.text_input("Nome completo", placeholder="Digite seu nome completo")
        username = st.text_input("Usuário", placeholder="Escolha um nome de usuário")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        if st.form_submit_button("Cadastrar"):
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
        
        if st.form_submit_button("Voltar para login"):
            st.session_state["pagina_atual"] = "login"
            st.session_state["page"] = "logout"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)