import streamlit as st

def format_brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def create_summary_card(title, value=None, color="#FF0000", info1="", info2="", info3=""):
    info1 = str(info1 or "")
    info2 = str(info2 or "")
    info3 = str(info3 or "")
    title = str(title or "")

    html = f"""
    <style>
        .summary-card {{
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.08);
            border: 1px solid #F0F0F0;
            width: 100%;
            min-height: 150px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .summary-card:hover {{
            transform: translateY(-5px); 
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15); 
        }}
        .grafico-titulo {{
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 12px;
        }}
    </style>
    <div class="summary-card">
        <h4 class="grafico-titulo">{title}</h4>
        <div style="color:#444;font-size:14px;line-height:1.6;">
            {info1}<br>{info2}<br>{info3}
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)