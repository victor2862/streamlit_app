# Importações
import streamlit as st
from src.db.app_db import AppDB


# Configuração da página inicial
st.set_page_config(
    page_title="Meu primeiro app",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


# Inicialização do banco de dados
if 'db' not in st.session_state:
    st.session_state.db = AppDB()
    st.session_state.db.inicializar_banco()
    st.session_state.db.inserir_projetos_exemplo()


# Criação das páginas e do menu de navegação
home = st.Page("src/pages/home.py", title="Home", icon=":material/home:")
projetos = st.Page("src/pages/projetos.py", title="Projetos", icon=":material/folder_open:")
visao_geral_projeto = st.Page("src/pages/visao_geral_projeto.py", title="Visão Geral", icon=":material/assessment:")

pg = st.navigation({
    "Início": [home, projetos],
    "Projetos": [visao_geral_projeto]
})

pg.run()



