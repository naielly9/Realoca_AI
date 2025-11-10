import streamlit as st

def indicador_card(titulo: str, valor: str, variacao: str = None, tipo: str = 'info', texto_lado: str = None, alerta: str = None):
    cores = {
        'up': '#d4f4dd',      
        'down': '#ffd6d6',     
        'warning': '#ffe7c3',  
        'info': "#7CABF3FF",   
        'custom': alerta or '#d4f4dd'
    }

    icones = {
        'up': '🡅',
        'down': '🡇',
        'info': 'ℹ️'
    }

    if tipo in ['up', 'down', 'info']:
        if tipo == 'up':
            cor_texto = 'green'
        elif tipo == 'down':
            cor_texto = 'red'
        elif tipo == 'info':
            cor_texto = '#004a99'  
        else:
            cor_texto = '#333'

        tag = f"""
        <span style="
            background-color: {cores[tipo]};
            color: {cor_texto};
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        ">
      {variacao}
        </span>
        """

        complemento = f"<span style='margin-left: 6px; color: #555;'>{texto_lado or ''}</span>"
    elif tipo == 'warning':
        tag = f"""
        <span style="background-color: {cores[tipo]}; color: orange; 
                     padding: 2px 6px; border-radius: 4px; font-weight: 500;">
            {variacao} 
        </span>
        """
        complemento = f"<span style='margin-left: 6px; color: #555;'>{texto_lado or ''}</span>"

    elif tipo == 'custom' and variacao:
        tag = f"""
        <span style="background-color: {cores['custom']}; color: white;
                     padding: 2px 6px; border-radius: 4px; font-weight: 500;">
            {variacao}
        </span>
        """
        complemento = f"<span style='margin-left: 6px; color: #555;'>{texto_lado or ''}</span>"

    else:
        tag = ""
        complemento = ""

    st.markdown(f"""
    <style>
        .kpi-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }}
        .kpi-card {{
        padding: 1rem;
        border: 1px solid #eee;
        border-radius: 8px;
        background-color: white;
        min-width: 160px;
        transition: all 0.2s ease-in-out;
        }}
        .kpi-title {{
        font-size: 1rem;
        color: #444;
        }}
        .kpi-value {{
        font-size: 1.8rem;
        font-weight: bold;
        }}
        .kpi-tag {{
        font-size: 0.8rem;
        font-weight: normal;
        color: #666;
        margin-left: 4px;
        }}
    </style>
    <div class="kpi-card">
    <div class="kpi-title">{titulo}</div>
    <div><span class="kpi-value">{valor}</span><span class="kpi-tag">{tag}</span></div>
    <div>{complemento}</div>
    </div>
    """, unsafe_allow_html=True)
