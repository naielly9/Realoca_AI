import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.components.indicador_card import indicador_card
from src.components.summary_card import create_summary_card
from src.components.grafico_barras import criar_grafico_barras
from streamlit_option_menu import option_menu

def mostrar_tela_analises(db):
    st.title("Gestão de Deslocamento e Filiais")
    db.deletar_funcionarios_sem_filial()
    df_filiais = db.get_filiais()
    df_func = db.get_funcionarios()

    st.markdown(
        """
        <style>
        .menu-container {
            position: sticky;
            top: 0;
            background-color: white;
            z-index: 999;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            width: 100%;
            left: 0;
            margin: 0;
        }
        .block-container {
            padding-left: 0rem;
            padding-right: 0rem;
        }
        .menu-container .nav.nav-pills {
            justify-content: space-around;
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    tab_titles = ["Realocação e Mobilidade", "Filiais e Cobertura", "Funcionários"]

    aba_ativa = option_menu(
        menu_title=None,
        options=tab_titles,
        icons=["geo-alt", "building", "people-fill"],
        orientation="horizontal",
        default_index=0,
    )

    if aba_ativa == "Realocação e Mobilidade":
        total_funcionarios = len(df_func)
        total_filiais = len(df_filiais)
        ativos = df_func['ativo'].sum()
        inativos = df_func.get('inativo', pd.Series([0])).sum()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('')
            indicador_card("Total", str(total_funcionarios), variacao="Funcionários", tipo="info")
          
        with col2:
            st.markdown('')
            indicador_card("Total", str(total_filiais), variacao="Filiais", tipo="up")
            
        with col3:
            st.markdown('')
            indicador_card("Ativos", str(ativos), variacao="Funcionários", tipo="warning")
        with col4:
            st.markdown('')
            indicador_card("Inativos", str(inativos), variacao="Funcionários", tipo="down")

        st.subheader("🗺️ Mapa de Funcionários e Filiais")

        if not df_func.empty and not df_filiais.empty:
            layer_filiais = pdk.Layer(
                "ScatterplotLayer",
                data=df_filiais,
                get_position='[longitude, latitude]',
                get_color='[0, 255, 0, 200]',  
                get_radius=120,
                pickable=True,
            )

            layer_funcionarios = pdk.Layer(
                "ScatterplotLayer",
                data=df_func,
                get_position='[longitude, latitude]',
                get_color='[0, 100, 255, 200]',  
                get_radius=80,
                pickable=True,
            )

            view_state = pdk.ViewState(
                latitude=df_func['latitude'].mean() if not df_func['latitude'].isna().all() else -23.2,
                longitude=df_func['longitude'].mean() if not df_func['longitude'].isna().all() else -45.9,
                zoom=10,
                pitch=0
            )

          
            st.pydeck_chart(pdk.Deck(
                layers=[layer_filiais, layer_funcionarios],
                initial_view_state=view_state,
                tooltip={"text": "{nome_filial} / {nome}"}
            ))


            st.markdown("🟩 **Verde:** Filiais &nbsp;&nbsp;&nbsp; 🟦 **Azul:** Funcionários")
        else:
            st.warning("Não há dados suficientes para gerar o mapa.")

    elif aba_ativa == "Filiais e Cobertura":
        st.markdown("")
        if not df_filiais.empty:
            df_filiais = df_filiais.sort_values(by="cidade")
             
            cols_per_row = 4
            for i in range(0, len(df_filiais), cols_per_row):
                cols = st.columns(cols_per_row)
                subset = df_filiais.iloc[i:i+cols_per_row]

                for col, (_, row) in zip(cols, subset.iterrows()):
                    with col:
                        create_summary_card(
                            title=row["nome_filial"],
                            info1=f"📍 Cidade: {row['cidade']}",
                            color="#0064FFC8"
                        )

                st.markdown("")
            fig_filiais = criar_grafico_barras(df_filiais, "cidade", "Distribuição de Filiais por Cidade", cor="#004080")
            if fig_filiais:
                st.plotly_chart(fig_filiais, use_container_width=True)
            st.map(df_filiais[['latitude', 'longitude']])     
        else:
            st.info("Nenhuma filial cadastrada no momento.")

    elif aba_ativa == "Funcionários":
        if not df_func.empty:
            df_func["centro_custo"] = df_func["centro_custo"].astype(str).str.strip()
            col1, col2 = st.columns([2, 1])

            with col1:
                filtro_cidade = st.selectbox(
                    "Filtrar por cidade:",
                    ["Todos"] + sorted(df_func['cidade'].dropna().unique().tolist()))

            with col2:
                filtro_status = st.selectbox(
                    "Status:",
                    ["Todos", "Ativos", "Inativos"]
                )

            df_filtered = df_func.copy()
            if filtro_cidade != "Todos":
                df_filtered = df_filtered[df_filtered['cidade'] == filtro_cidade]
            if filtro_status == "Ativos":
                df_filtered = df_filtered[df_filtered['ativo'] == 1]
            elif filtro_status == "Inativos":
                df_filtered = df_filtered[df_filtered['ativo'] == 0]

            st.dataframe(
                df_filtered[['nome', 'mt', 'centro_custo', 'nome_filial', 'cidade', 'ativo']]
                .rename(columns={
                    'nome': 'Nome',
                    'mt': 'Matrícula',
                    'centro_custo': 'Centro de Custo',
                    'nome_filial': 'Filial',
                    'cidade': 'Cidade',
                    'ativo': 'Ativo'
                }),
                hide_index=True,
                use_container_width=True
            )


            st.divider()
            fig_func = criar_grafico_barras(df_func, "centro_custo", "Funcionários por Centro de Custo", cor="#004080") 
            st.plotly_chart(fig_func, use_container_width=True)
        else:
            st.warning("Nenhum funcionário cadastrado.")
