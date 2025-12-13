# Importações
import streamlit as st
from streamlit import session_state as sst
from src.db.app_db import AppDB
from src.ai.app_ai import AppAI
import src.utils.ui as ui


# Configuração da página inicial
st.set_page_config(
    page_title="Meu primeiro app",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")


# Inicialização das variáveis de sessão
if 'projeto_atual' not in sst:
    sst.projeto_atual = None
if 'contexto_atual' not in sst:
    sst.contexto_atual = None


# Inicialização de variáveis auxiliares
if 'contexto_visualizado' not in sst:
    sst.contexto_visualizado = None


# Inicialização de variáveis do sistema
if 'db' not in sst:
    sst.db = AppDB()
    sst.db.inicializar_banco()

if 'ai' not in sst:
    sst.ai = AppAI()


# Criação das páginas
pag_home = st.Page("src/pages/home.py", title="Home", icon=":material/home:")
pag_projetos = st.Page("src/pages/projetos.py", title="Projetos", icon=":material/folder_open:")
pag_visao_geral = st.Page("src/pages/visao_geral.py", title="Visão Geral", icon=":material/assessment:")
pag_contexto = st.Page("src/pages/contexto.py", title="Gestão de contexto", icon=":material/book:")
pag_config = st.Page("src/pages/configuracoes.py", title="Configurações", icon=":material/settings:")


# Criação do menu de navegação
try: header_projetos = sst.projeto_atual['nome']
except: header_projetos = "Nenhum projeto carregado"

pg = st.navigation({
    "Início": [pag_home, pag_projetos],
    header_projetos: [pag_visao_geral, pag_contexto],
    "Sistema": [pag_config]
})


# Execução do sistema
ui.exibir_mensagens()
pg.run()