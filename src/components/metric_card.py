from matplotlib.colors import to_rgb
import streamlit as st


def hex_to_rgba(hex_color, alpha=1.0):
    rgb = to_rgb(hex_color)
    r, g, b = [int(x * 255) for x in rgb]
    return f"rgba({r}, {g}, {b}, {alpha})"


def format_value(value, format_type=None):
    if format_type == "inteiro":
        return f"{int(value)}"
    elif format_type == "porcentagem":
        return f"{value:.1%}"
    elif format_type == "moeda":
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return str(value)


def create_metric_card(title, value, color="#004080", format_type=None):
    hover_background_color = hex_to_rgba(color, alpha=0.1)
    card_id = title.lower().replace(" ", "-").replace(":", "")

    formatted_value = format_value(value, format_type)

    st.markdown(f"""
    <div id="{card_id}" class="metric-card" style="border-left: 8px solid {color}; padding: 10px; margin-bottom: 10px; background: #ffffff; border-radius: 8px; transition: background-color 0.3s ease;">
        <div class="card-title" style="font-size: 16px; font-weight: 600;">{title}</div>
        <div class="card-value" style="color: {color}; font-weight: bold; font-size: 22px;">{formatted_value}</div>
    </div>
    <style>
    #{card_id}:hover {{
        background-color: {hover_background_color} !important;
        cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)
