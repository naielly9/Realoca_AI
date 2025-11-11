import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from database import Database
from src.services.realocacao_service import calcular_rotas
db = Database()
db.criar_tabelas()

def mostrar_tela_custo_transporte():
    def guess_column(df, keywords):
        """Retorna o nome da coluna do df que contém uma das keywords (case-insensitive) ou None."""
        cols = list(df.columns)
        low = [c.lower() for c in cols]
        for kw in keywords:
            for i, c in enumerate(low):
                if kw.lower() in c:
                    return cols[i]
        return None

    def ensure_session():
        if "usuario" not in st.session_state:
            st.session_state.usuario = {"nome": "Usuário Exemplo", "empresa": "Empresa Exemplo"}
        if "arquivo_lido" not in st.session_state:
            st.session_state.arquivo_lido = False
            st.session_state.df = pd.DataFrame()
            st.session_state.selecoes = {}  

    ensure_session()
    st.markdown("""
    <style>
    /* Container geral */
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
            <span class="material-icons">swap_horiz</span>
            <span>Realocação de Funcionários</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
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
        uploaded = st.file_uploader("Enviar arquivo Excel", type=["xls", "xlsx"], key="uploader")


    st.markdown('</div>', unsafe_allow_html=True)
            
    def to_excel(df, totais=None):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_to_export = df.copy()

                        if totais is not None:
                            total_row = {col: "" for col in df_to_export.columns}  
                            for col in totais.index:
                                if col in df_to_export.columns:
                                    total_row[col] = totais[col]
                            df_to_export = pd.concat(
                                [df_to_export, pd.DataFrame([total_row])],
                                ignore_index=True
                            )

                            first_col = df_to_export.columns[0]
                            df_to_export.loc[df_to_export.index[-1], first_col] = "TOTAL"

                        df_to_export.to_excel(writer, index=False, sheet_name="Colaboradores")

                    output.seek(0)
                    return output
    
    if uploaded is not None:
        if "ultimo_upload" not in st.session_state or uploaded.name != st.session_state.ultimo_upload:
            try:
                df_uploaded = pd.read_excel(uploaded)
                mt_importadas = []

                for _, row in df_uploaded.iterrows():
                    nome_func = str(row.get("NOME") or f"Funcionario_{row.get('ID')}").strip()
                    id_filial = str(row.get("FILIAL") or "").strip()
                    mt = str(row.get("MT") or "").strip()
                    centro_custo = str(row.get("C CUSTO") or row.get("CENTRO CUSTO") or "").strip()
                    estado = str(row.get("ESTADO") or row.get("Estado") or "").strip()
                    municipio = str(row.get("MUNICIPIO") or row.get("Municipio") or "").strip()
                    bairro = str(row.get("BAIRRO") or row.get("Bairro") or "").strip()
                    cep = str(row.get("CEP") or row.get("Cep") or "").replace("-", "").strip()
                    logradouro = str(row.get("ENDERECO") or row.get("Endereço") or "").strip()
                    numero = str(row.get("Num.Endereço") or "").strip()
                
                    if mt:
                        estado_id = db.get_or_create_estado(estado, estado)
                        cidade_id = db.get_or_create_cidade(municipio, estado_id)
                        bairro_id = db.get_or_create_bairro(bairro, cidade_id)
                        endereco_id = db.get_or_create_endereco(logradouro, numero, cep, bairro_id)
                        db.get_or_create_funcionario(nome_func, endereco_id, id_filial, mt, centro_custo)
                        mt_importadas.append(mt)

                if mt_importadas:
                    df = calcular_rotas(mt_importadas)
                    st.session_state.df = df.copy()
                    st.session_state.arquivo_lido = True
                    st.session_state.ultimo_upload = uploaded.name
                    st.session_state.selecoes = {}
             
            except Exception as ex:
                st.error(f"Erro ao ler o Excel: {ex}")
                st.session_state.arquivo_lido = False

    if "df" in st.session_state and st.session_state.arquivo_lido:
        df = st.session_state.df.copy()

        mt_col = guess_column(df, ["mt"])
        if mt_col is None:
            st.warning("Coluna 'MT' não encontrada no arquivo.")
            st.stop()

        ccusto_col = guess_column(df, ["c custo", "c_custo", "ccusto"])
        endereco_col = guess_column(df, ["endereco colaborador", "endereço colaborador", "endereco"])
        onde_col = guess_column(df, ["onde estava", "onde estava alocado", "alocado", "filial"])
        antiga_dist_col = guess_column(df, ["destino0", "distancia0", "antiga distancia", "antiga distância"])
        destino_atual = guess_column(df, ["Destino atual"])

        dest_cols = [guess_column(df, [f"destino{i}"]) for i in range(1, 4)]
        dist_cols = [guess_column(df, [f"distancia{i}"]) for i in range(1, 4)]
        red_cols = [guess_column(df, [f"Redução {i}", f"Redução {i}"]) for i in range(1, 4)]

        df["Colaborador"] = df[mt_col].astype(str).fillna("")

        rows = []
        for _, row in df.iterrows():
            agrup = row["Colaborador"]
            for i in range(3):
                if dest_cols[i] and dest_cols[i] in df.columns:
                    rows.append({
                        "Colaborador": agrup,
                        "Selecionar": 'Selecionar ✅',
                        "Centro de Custo": row.get(ccusto_col, ""),
                        "Destino Atual": row.get(destino_atual, ""),
                        "Antiga Distância": row.get(antiga_dist_col, ""),
                        "Novo Destino": row.get(dest_cols[i], ""),
                        "Distância Nova (km)": row.get(dist_cols[i], ""),
                        "Redução %": row.get(red_cols[i], ""),
                        "Opção": f"Destino {i+1}"
                    })

        detail_df = pd.DataFrame(rows)
        detail_df["Colaborador"] = detail_df["Colaborador"].fillna("")
        column_widths = {}
        for col in detail_df.columns:
            max_len_content = detail_df[col].astype(str).apply(len).max() if not detail_df[col].empty else 0
            max_len_header = len(str(col))
            calculated_width = max(max_len_header * 10 + 20, max_len_content * 8 + 20)
            column_widths[col] = calculated_width
        
        gb = GridOptionsBuilder.from_dataframe(detail_df)
        gb.configure_column(
            "Colaborador",
            rowGroup=True,
            hide=True,
            minWidth=int(column_widths.get("Colaborador", 300))
        )
        gb.configure_column(
            "Selecionar",
            headerName="",  
            minWidth=150,
            cellStyle={"textAlign": "center"},
        )
        gb.configure_column("Novo Destino", minWidth=220)
        gb.configure_column("Distância Nova (km)", type=["numericColumn"])
        gb.configure_column(
            "Redução %",
            type=["numericColumn"],
            minWidth=100,
            valueFormatter=JsCode("function(params) { return params.value ? params.value.toFixed(2) : ''; }"),
        )
        gb.configure_column("Opção", minWidth=120)
        
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)

        gb.configure_selection(
            selection_mode="single", 
            use_checkbox=True,
            groupSelectsChildren=False, 
            groupSelectsFiltered=False   
        )

        gb.configure_grid_options(
            groupDisplayType="multipleColumns",
            suppressRowClickSelection=False,
            groupSelectsChildren=False,      
            rowSelection='single',
            suppressRowDeselection=False
        )

        if "df_excel" not in st.session_state or st.session_state.df_excel is None:
            st.session_state.df_excel = detail_df

        grid_options = gb.build()
        grid_options["domLayout"] = "normal"
        grid_options["aggFuncs"] = {"sum": "sum", "avg": "avg", "count": "count"}  

        btn_export_placeholder = st.empty()  
        grid_response = AgGrid(
            detail_df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=False,
            theme="alpine",
            height=550,
            allow_unsafe_jscode=True,
            show_search= True,
            show_download_button= True
        )
        

        selected_rows = grid_response.get("selected_rows", [])
        if not st.session_state.get("selecoes_grid"):
            st.session_state["selecoes_grid"] = []

        if isinstance(selected_rows, dict):
            selected_rows = [selected_rows]
    
        if isinstance(selected_rows, pd.DataFrame):
            if not selected_rows.empty:
                selected_row = selected_rows.iloc[0].to_dict() 
                mt_col = "Colaborador"  
                existing_index = next(
                    (i for i, item in enumerate(st.session_state["selecoes_grid"]) if item[mt_col] == selected_row[mt_col]),
                    None
                )

                if existing_index is not None:
                    st.session_state["selecoes_grid"][existing_index] = selected_row
                else:
                    st.session_state["selecoes_grid"].append(selected_row)

        if st.session_state.get("selecoes_grid"):
            selecoes_df = pd.DataFrame(st.session_state["selecoes_grid"])          
            df_export = selecoes_df.copy()

            cols_state = getattr(grid_response, "columns_state", None) or []
            cols_visiveis_ordenadas = [c["colId"] for c in cols_state if not c.get("hide")]
            if cols_visiveis_ordenadas:
                df_export = df_export[[c for c in cols_visiveis_ordenadas if c in df_export.columns]]
            st.session_state.df_excel = df_export

            btn_export_placeholder.download_button(
                label="📥 Exportar Excel",
                data=to_excel(st.session_state.df_excel),
                file_name="dados_filtrados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    