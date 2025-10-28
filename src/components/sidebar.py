import streamlit as st

def sidebar_menu():
    st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<style>
.sidebar-container {
    background-color: #1f2525;
    height: 100vh;
    color: #dddee0;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: width 0.3s ease;
    overflow-x: hidden;
    border-right: 1px solid #333;
    padding-top: 10px;
}
.menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 15px;
    border-radius: 10px;
    cursor: pointer;
    transition: background-color 0.3s;
    width: 100%;
    justify-content: flex-start;
}
.menu-item:hover {
    background-color: #2e3333;
}
.menu-icon {
    color: #dddee0;
    font-size: 22px;
}
.menu-text {
    font-size: 15px;
    color: #dddee0;
    white-space: nowrap;
}
.toggle-btn > button {
    background-color: transparent !important;
    border: none !important;
    color: #dddee0 !important;
    font-size: 18px !important;
    padding: 0 !important;
    margin-bottom: 15px;
}
.menu-btn > button {
    background-color: transparent !important;
    border: none !important;
    text-align: left !important;
    width: 100% !important;
    color: #dddee0 !important;
}
</style>
""", unsafe_allow_html=True)
    
    with st.sidebar:
        with st.container():
            st.markdown("""
    <style>
    [data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: absolute !important;
        top: 10px !important;
        right: 10px !important;
        z-index: 9999 !important;
    }

    [data-testid="stSidebarCollapseButton"] button {
        background-color: #f5f6f8 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        transition: background-color 0.2s ease;
    }

    [data-testid="stSidebarCollapseButton"] button:hover {
        background-color: #e2e2e2 !important;
    }

    [data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"] {
        opacity: 1 !important;
        visibility: visible !important;
        color: #333 !important;
    }
    </style>
""", unsafe_allow_html=True)
            
            st.markdown("""
      <style>
      [data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"] {
          color: transparent !important;
          position: relative;
      }

      [data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"]::before {
          content: "menu";                     
          font-family: "Material Icons";     
          font-size: 22px;
          line-height: 1;
          display: inline-block;
          position: absolute;
          left: 0;
          top: 50%;
          transform: translateY(-50%);
          -webkit-font-smoothing: antialiased;
          /* fallback color */
          color: #444;
      }
      [data-testid="stExpandSidebarButton"] span[data-testid="stIconMaterial"] {
          color: transparent !important;
          position: relative;
      }

      [data-testid="stExpandSidebarButton"] span[data-testid="stIconMaterial"]::before {
          content: "menu"; /* ou "chevron_right", "arrow_forward", etc */
          font-family: "Material Icons";     
          font-size: 22px;
          line-height: 1;
          display: inline-block;
          position: absolute;
          left: 0;
          top: 50%;
          transform: translateY(-50%);
          -webkit-font-smoothing: antialiased;
          color: #444;
      }
      [data-testid="stSidebarContent"] {
    overflow: hidden !important;   
}

[data-testid="stSidebar"] {
    overflow: hidden !important;   
}
      </style>
""", unsafe_allow_html=True)
            
            def styled_menu_button(key: str, icon: str, label_text: str, page_value: str):
                st.markdown(f"""
                <style>
                .st-key-{key} button {{
                    all: unset !important;             
                    display: flex !important;
                    align-items: center !important;
                    gap: 12px !important;
                    width: 100% !important;
                    padding: 10px 18px !important;
                    border-radius: 6px !important;
                    font-family: "Inter", sans-serif !important;
                    font-size: 15px !important;
                    font-weight: 500 !important;
                    color: #1e1e1e !important;
                    cursor: pointer !important;
                    transition: background-color 0.2s ease, color 0.2s ease !important;
                    background: none !important;
                    text-align: left !important;
                }}

                .st-key-{key} button:hover {{
                    background-color: #505050 !important;
                    color: #ffffff !important;
                }}

        </style>
        """, unsafe_allow_html=True)

                label = f":material/{icon}:  {label_text}"
            
                if st.button(label, key=key, use_container_width=True):
                    st.session_state["page"] = page_value
                    
            styled_menu_button("btn_analises", "analytics", "Análises", "analises")
            styled_menu_button("btn_user", "person_add", "Cadastro de Usuário", "usuario")
            styled_menu_button("btn_func", "group", "Cadastro de Fúncionarios e Filiais", "funcionarios")
            styled_menu_button("btn_transporte", "local_shipping", "Custo de Transporte", "transporte")
            

            st.markdown(f"""
            <style>
            .st-key-btn_logout button
            {{
                all: unset !important;             
                display: flex !important;
                align-items: center !important;
                gap: 12px !important;
                width: 100% !important;
                padding: 10px 18px !important;
                border-radius: 6px !important;
                font-family: "Inter", sans-serif !important;
                font-size: 15px !important;
                font-weight: 500 !important;
                color: #1e1e1e !important;
                cursor: pointer !important;
                transition: background-color 0.2s ease, color 0.2s ease !important;
                background: none !important;
                text-align: left !important;
            }}
            .st-key-btn_logout button:hover {{
                    background-color: #505050 !important;
                    color: #ffffff !important;
                }}
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            logout_icon = "logout"  
            label_logout = f":material/{logout_icon}:  Sair"
        

            if st.button(label_logout, key="btn_logout", use_container_width=True):
                print("logout sidebar")
                st.session_state["page"] = "logout"
                st.rerun()