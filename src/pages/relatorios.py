import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.components.indicador_card import indicador_card
from src.components.summary_card import create_summary_card
def mostrar_tela_analises(db):

    st.title("📊 Dashboard de Realocação de Funcionários")
    db.deletar_funcionarios_sem_filial()
    df_filiais = db.get_filiais()
    df_func = db.get_funcionarios()

    tab1, tab2, tab3 = st.tabs(["🧭 Realocação e Mobilidade", "🏢 Filiais e Cobertura", "👥 Funcionários"])
    st.markdown("""
        <style>
            .main-container {
                padding: 1rem 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    with tab1:
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

        

    with tab2:
        st.markdown("")
        if not df_filiais.empty:
            df_filiais = df_filiais.sort_values(by="cidade")
             
            def criar_grafico_filiais(df):
                df_cidades = df["cidade"].value_counts().reset_index()
                df_cidades.columns = ["Cidade", "Quantidade de Filiais"]

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_cidades["Cidade"],
                    y=df_cidades["Quantidade de Filiais"],
                    marker_color="#004080",
                    text=df_cidades["Quantidade de Filiais"],
                    textposition="auto",
                    hoverinfo="text",
                    hovertext=[f"Cidade: {c}<br>Filiais: {q}" for c, q in zip(df_cidades["Cidade"], df_cidades["Quantidade de Filiais"])]
                ))

                fig.update_layout(
                    title=dict(
                        text="<b>Distribuição de Filiais por Cidade</b>",
                        x=0.5,
                        xanchor="center",
                        font=dict(size=16, family="Arial", color="black")
                    ),
                    xaxis_title="Cidade",
                    yaxis_title="Quantidade de Filiais",
                    xaxis=dict(
                        tickangle=0,
                        tickfont=dict(size=12, family="Arial")
                    ),
                    yaxis=dict(
                        tickfont=dict(size=12, family="Arial"),
                        dtick=1
                    ),
                    plot_bgcolor="white",
                    hoverlabel=dict(bgcolor="#497CAF", font_size=12, font_color="white"),
                    margin=dict(l=50, r=30, t=80, b=50)
                )

                return fig
           
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
            fig = criar_grafico_filiais(df_filiais)
            st.plotly_chart(fig, use_container_width=True)
            st.map(df_filiais[['latitude', 'longitude']])     
        else:
            st.info("Nenhuma filial cadastrada no momento.")

    with tab3:
        st.subheader("👥 Funcionários por Centro de Custo")
        if not df_func.empty:
            st.bar_chart(df_func['centro_custo'].value_counts())

            st.divider()
            st.subheader("📋 Lista de Funcionários")
            filtro_cidade = st.selectbox("Filtrar por cidade:", ["Todos"] + sorted(df_func['cidade'].dropna().unique().tolist()))
            filtro_status = st.radio("Status", ["Todos", "Ativos", "Inativos"], horizontal=True)

            df_filtered = df_func.copy()
            if filtro_cidade != "Todos":
                df_filtered = df_filtered[df_filtered['cidade'] == filtro_cidade]
            if filtro_status == "Ativos":
                df_filtered = df_filtered[df_filtered['ativo'] == 1]
            elif filtro_status == "Inativos":
                df_filtered = df_filtered[df_filtered['ativo'] == 0]

            st.dataframe(
                df_filtered[['nome', 'mt', 'centro_custo', 'nome_filial', 'cidade', 'ativo']].rename(
                    columns={
                        'nome': 'Nome',
                        'mt': 'Matrícula',
                        'centro_custo': 'Centro de Custo',
                        'nome_filial': 'Filial',
                        'cidade': 'Cidade',
                        'ativo': 'Ativo'
                    }
                ),
                use_container_width=True
            )

        else:
            st.warning("Nenhum funcionário cadastrado.")
