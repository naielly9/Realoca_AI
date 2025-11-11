import plotly.graph_objects as go

def criar_grafico_barras(df, coluna, titulo, cor="#004080"):
    """Cria um gráfico de barras genérico a partir de uma coluna."""
    if df.empty or coluna not in df.columns:
        return None

    df_contagem = df[coluna].value_counts().reset_index()
    df_contagem.columns = [coluna.capitalize(), "Quantidade"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_contagem[coluna.capitalize()],
        y=df_contagem["Quantidade"],
        marker_color=cor,
        text=df_contagem["Quantidade"],
        textposition="auto",
        hoverinfo="text",
        hovertext=[
            f"{coluna.capitalize()}: {c}<br>Quantidade: {q}"
            for c, q in zip(df_contagem[coluna.capitalize()], df_contagem["Quantidade"])
        ]
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{titulo}</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=16, family="Arial", color="black")
        ),
        xaxis_title=coluna.capitalize(),
        yaxis_title="Quantidade",
        xaxis=dict(
            type="category",
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
