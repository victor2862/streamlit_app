# Importações
import streamlit as st
from src.db.app_db import AppDB


# Configuração da página inicial
st.set_page_config(
    page_title="Meu primeiro app",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto")


# Inicialização das tags de mensagem
if 'msg_projeto_criado' not in st.session_state:
    st.session_state.msg_projeto_criado = 0
if 'msg_projeto_carregado' not in st.session_state:
    st.session_state.msg_projeto_carregado = 0
if 'msg_projeto_deletado' not in st.session_state:
    st.session_state.msg_projeto_deletado = 0
if 'msg_contexto_restaurado' not in st.session_state:
    st.session_state.msg_contexto_restaurado = 0
if 'msg_contexto_editado' not in st.session_state:
    st.session_state.msg_contexto_editado = 0


# Inicialização das variáveis de sessão
if 'projeto_atual' not in st.session_state:
    st.session_state.projeto_atual = None
if 'contexto_atual' not in st.session_state:
    st.session_state.contexto_atual = None


# Inicialização de variáveis auxiliares
if 'contexto_visualizado' not in st.session_state:
    st.session_state.contexto_visualizado = None


# Inicialização do banco de dados
if 'db' not in st.session_state:
    st.session_state.db = AppDB()
    st.session_state.db.inicializar_banco()


# Criação das páginas e do menu de navegação
pag_home = st.Page("src/pages/home.py", title="Home", icon=":material/home:")
pag_projetos = st.Page("src/pages/projetos.py", title="Projetos", icon=":material/folder_open:")
pag_visao_geral = st.Page("src/pages/visao_geral.py", title="Visão Geral", icon=":material/assessment:")
pag_contexto = st.Page("src/pages/contexto.py", title="Gestão de contexto", icon=":material/book:")


try: header_projetos = st.session_state.projeto_atual['nome']
except: header_projetos = "Nenhum projeto carregado"

pg = st.navigation({
    "Início": [pag_home, pag_projetos],
    header_projetos: [pag_visao_geral, pag_contexto]
})

pg.run()