import streamlit as st
import pandas as pd


def mostrar_tela_cadastro_enderecos(db):
    st.title("Cadastro de Endereços de Filiais e Funcionários")

    if "usuario" not in st.session_state:
        st.session_state.usuario = {"nome": "Usuário Exemplo", "empresa": "Empresa Exemplo"}

    col1, col2 = st.columns([3, 3])
    with col1:
        st.markdown("### 👤 Usuário")
        st.write(st.session_state.usuario["nome"])
    with col2:
        st.markdown("### 🏢 Empresa")
        #st.write(st.session_state.usuario["empresa"])

    st.divider()

    st.markdown("### 📤 Importar Planilha")
    uploaded = st.file_uploader(
        "Envie o Excel (xls/xlsx) com os endereços de filiais ou funcionários",
        type=["xls", "xlsx"]
    )

    if not uploaded:
        st.info("Envie uma planilha para continuar.")
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