import streamlit as st
import pandas as pd


def mostrar_tela_cadastro_enderecos(db):
    st.markdown("""
    <style>
    .main-container {
        padding: 1rem 2rem;
    }

    .painel-header {
        display: flex;
        justify-content: space-between;
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

    .label-custom {
        font-size: 0.85rem;
        color: #444;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 4px;
    }

    .material-icons {
        font-size: 1.2rem;
        color: #004080;
    }

    section[data-testid="stFileUploader"] label div {
        background-color: #f5f5f5;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 0.3rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 500;
        transition: 0.2s;
    }

    section[data-testid="stFileUploader"] label div:hover {
        background-color: #e0e0e0;
        border-color: #999;
    }
    </style>

    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="painel-header">
        <div class="titulo-pagina">
            <span class="material-icons">location_city</span>
            <span>Cadastro de Endereços de Filiais e Funcionários</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "usuario" not in st.session_state:
        st.session_state.usuario = {"nome": "Usuário Exemplo"}

    col1, col2 = st.columns([3, 3])

    with col1:
        st.markdown(
            "<div class='label-custom'><span class='material-icons'>person</span><b>Usuário</b></div>",
            unsafe_allow_html=True
        )
        st.write(st.session_state.usuario["nome"])

    with col2:
        st.markdown(
            "<div class='label-custom'><span class='material-icons'>upload_file</span><b>Importar Planilha</b></div>",
            unsafe_allow_html=True
        )
        uploaded = st.file_uploader(
            "Envie o arquivo Excel com os endereços de filiais ou funcionários",
            type=["xls", "xlsx"],
            key="upload_enderecos"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if not uploaded:
        return

    try:
        df = pd.read_excel(uploaded)
        st.success(f"Arquivo '{uploaded.name}' carregado com sucesso.")
        st.dataframe(df.head(5))
    except Exception as e:
        st.error(f"Erro ao ler o Excel: {e}")
        return

    st.divider()

    cols_lower = [c.lower() for c in df.columns]
    tipo = None
    if "id_filial" in cols_lower:
        tipo = "filial"
    elif "id" in cols_lower and "filial" in cols_lower:
        tipo = "funcionario"

    if tipo is None:
        st.error("Não foi possível identificar se a planilha é de filiais ou funcionários.")
        return

    if st.button("📥 Cadastrar no Banco de Dados"):
        with st.spinner("Cadastrando dados..."):
            inseridos = {"estados": 0, "cidades": 0, "bairros": 0, "enderecos": 0, "filiais": 0, "funcionarios": 0}

            for _, row in df.iterrows():
                estado = str(row.get("ESTADO") or row.get("Estado")).strip()
                municipio = str(row.get("MUNICIPIO") or row.get("Municipio")).strip()
                bairro = str(row.get("BAIRRO") or row.get("Bairro")).strip()
                cep = str(row.get("CEP") or row.get("Cep")).replace("-", "").strip()
                logradouro = str(row.get("ENDERECO") or row.get("Endereço")).strip()
                numero = str(row.get("Num.Endereço") or "").strip()
                mt = str(row.get("MT") or "").strip()
                centro_custo = str(row.get("C CUSTO") or row.get("CENTRO CUSTO") or "").strip()

                estado_id = db.get_or_create_estado(estado, estado)
                cidade_id = db.get_or_create_cidade(municipio, estado_id)
                bairro_id = db.get_or_create_bairro(bairro, cidade_id)
                endereco_id = db.get_or_create_endereco(logradouro, numero, cep, bairro_id)

                if tipo == "filial":
                    nome_filial = str(row.get("ID_FILIAL")).strip()
                    db.get_or_create_filial(nome_filial, endereco_id)
                    inseridos["filiais"] += 1
                else:
                    nome_func = str(row.get("NOME") or f"Funcionario_{row.get('ID')}").strip()
                    id_filial = str(row.get("FILIAL") or "").strip()
                    mt = str(row.get("MT") or "").strip()
                    centro_custo = str(row.get("C CUSTO") or row.get("CENTRO CUSTO") or "").strip()

                    db.get_or_create_funcionario(nome_func, endereco_id, id_filial, mt, centro_custo)
                    inseridos["funcionarios"] += 1

            st.success("✅ Cadastro concluído!")
            st.json(inseridos)