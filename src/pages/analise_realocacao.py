import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

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
            st.session_state.selecoes = {}  # { MT: { 'empresa':..., 'distancia_km':..., 'reducao':... } }

    def df_summary_for_display(df):
        # cria um resumo com as colunas esperadas, preenchendo com '-' quando não existe
        col_map = {
            "MT": ["mt"],
            "C CUSTO": ["c custo", "c_custo", "ccusto", "c custo"],
            "Endereço Colaborador": ["endereco", "endereço", "endereco colaborador", "endereço colaborador"],
            "Onde Estava Alocado": ["onde estava", "onde estava alocado", "alocado", "filial"],
            "Antiga Distância (Destino 0)": ["destino0", "destino 0", "distancia0", "distancia 0", "antiga distancia", "antiga distância", "destino0_distancia"]
        }

        out = pd.DataFrame()
        for out_col, keys in col_map.items():
            col = guess_column(df, keys)
            out[out_col] = df[col] if col else ["-"] * len(df)
        return out

    def gerar_pdf_bytes(selecoes_dict):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Relatório de Realocações")
        y -= 30
        c.setFont("Helvetica", 12)
        if not selecoes_dict:
            c.drawString(50, y, "Nenhuma seleção realizada.")
        else:
            for mt, sel in selecoes_dict.items():
                texto = f"{mt} → {sel.get('empresa','-')} | Distância: {sel.get('distancia_km','-')} km | Redução: {sel.get('reducao','-')}"
                c.drawString(50, y, texto)
                y -= 18
                if y < 60:
                    c.showPage()
                    y = height - 50
        c.save()
        buffer.seek(0)
        return buffer

    ensure_session()

    # Cabeçalho
    col1, col2, col3 = st.columns([3, 3, 2])
    with col1:
        st.markdown("### 👤 Usuário")
        st.write(st.session_state.usuario["nome"])
    with col2:
        st.markdown("### 🏢 Empresa")
        #st.write(st.session_state.usuario["empresa"])
    with col3:
        st.markdown("### ⬆ Upload")
        uploaded = st.file_uploader("Envie o Excel (xls/xlsx) com todos os campos", type=["xls", "xlsx"], key="uploader")

    st.divider()

    if uploaded is not None:
        try:
            df = pd.read_excel(uploaded)
            st.session_state.df = df.copy()
            st.session_state.arquivo_lido = True
            # limpa seleções anteriores
            st.session_state.selecoes = {}
            st.success("Planilha carregada com sucesso.")
        except Exception as ex:
            st.error(f"Erro ao ler o Excel: {ex}")
            st.session_state.arquivo_lido = False

    # opção mock (útil para testar sem arquivo)
    if st.button("🔁 Carregar planilha mock (teste)", help="Gera uma planilha de exemplo para testar a UI"):
        st.session_state.df = pd.DataFrame(
            [
                {
                    "MT": "MT 177",
                    "C CUSTO": "C1",
                    "Endereco Colaborador": "R GERALDO CAMPOS MOREIRA, 375",
                    "Onde Estava Alocado": "BROOKLIN NOVO",
                    "Antiga Distância (Destino 0)": 47.016,
                    "Destino1": "AV ITAQUERA 7426, VILA CARMOSINA",
                    "Distancia1": 8.772,
                    "Reducao1": "-81%",
                    "Destino2": "AV GUILHERME COTCHING 1877-1901, VILA MARIA",
                    "Distancia2": 19.426,
                    "Reducao2": "-59%",
                    "Destino3": "R DOUTOR ALMEIDA LIMA, 1124, MOOCA",
                    "Distancia3": 22.41,
                    "Reducao3": "-52%",
                },
                {
                    "MT": "MT 6030",
                    "C CUSTO": "C2",
                    "Endereco Colaborador": "AV CORIFEU DE AZEVEDO MARQUES 950",
                    "Onde Estava Alocado": "BUTANTA",
                    "Antiga Distância (Destino 0)": 22.42,
                    "Destino1": "R MANOEL DA NOBREGA, 712, DIADEMA",
                    "Distancia1": 5.936,
                    "Reducao1": "-74%",
                    "Destino2": "RUA CAPITAO THIAGO LUZ, 15, SANTO AMARO",
                    "Distancia2": 7.475,
                    "Reducao2": "-67%",
                    "Destino3": "AV LUCAS NOGUEIRA GARCEZ, 400, SBC",
                    "Distancia3": 14.509,
                    "Reducao3": "-35%",
                },
            ]
        )
        st.session_state.arquivo_lido = True
        st.session_state.selecoes = {}
        st.success("Mock carregado.")

    if not st.session_state.arquivo_lido:
        st.info("Aguardando upload de planilha. A planilha deve conter as colunas com MT, C CUSTO, Endereço Colaborador, Onde Estava Alocado, Antiga Distância (Destino 0), Destino1/Distancia1/Reducao1, Destino2/..., Destino3/...")
        st.stop()

    df = st.session_state.df.copy()
    mt_col = guess_column(df, ["mt"])
    ccusto_col = guess_column(df, ["c custo", "c_custo", "ccusto"])
    endereco_col = guess_column(df, ["endereco colaborador", "endereço colaborador", "endereco"])
    onde_col = guess_column(df, ["onde estava", "onde estava alocado", "alocado", "filial"])
    antiga_dist_col = guess_column(df, ["destino0", "distancia0", "antiga distancia", "antiga distância"])

    dest_cols = [guess_column(df, [f"destino{i}"]) for i in range(1, 4)]
    dist_cols = [guess_column(df, [f"distancia{i}"]) for i in range(1, 4)]
    red_cols = [guess_column(df, [f"Redução {i}", f"Redução {i}"]) for i in range(1, 4)]

    df["Colaborador"] = (
        df[mt_col].astype(str).fillna("") + " | " +
        (df[ccusto_col].astype(str).fillna("") if ccusto_col else "") + " | " +
        (df[endereco_col].astype(str).fillna("") if endereco_col else "") + " | " +
        (df[onde_col].astype(str).fillna("") if onde_col else "") + " | " +
        (df[antiga_dist_col].astype(str).fillna("") if antiga_dist_col else "")
    )
    
    rows = []
    for idx, row in df.iterrows():
        agrup = row["Colaborador"]
        mt_val = row[mt_col] if mt_col else ""
        for i in range(3):
            if dest_cols[i] and dest_cols[i] in df.columns:
                rows.append({
                    "Colaborador": agrup,
                    "Selecionar": 'Selecionar ✅',
                    "MT":mt_val,
                    "Novo Destino": row.get(dest_cols[i], ""),
                    "Distância Nova (km)": row.get(dist_cols[i], ""),
                    "Redução": row.get(red_cols[i], ""),
                    "Opção": f"Destino {i+1}"
                })

    detail_df = pd.DataFrame(rows)
    st.markdown("### 📋 Tabela de Realocação (expanda um MT para ver opções de destino)")

    detail_df["Colaborador"] = detail_df["Colaborador"].fillna("")
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
        "Redução",
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
            mt_col = "MT"  
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
        print('selecoes df',selecoes_df)           
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

    