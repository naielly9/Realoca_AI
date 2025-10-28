import streamlit as st
from pathlib import Path

LOGO_PATH = Path(__file__).parent.parent / "assets" / "logo" / "logo_realoca_ai.png"

PRIMARY_COLOR = "#003366"
SECONDARY_COLOR = "#0099cc"

def exibir_logo():
    st.image(str(LOGO_PATH), width=180)
