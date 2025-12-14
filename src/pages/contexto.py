import pandas as pd
import streamlit as st
from streamlit import session_state as sst
from datetime import datetime
import src.utils.ui as ui


# Diálogo de geração de contexto
@st.dialog("Gerar contexto", width="large")
def gerar_contexto():
    pass


# Diálogo de edição de contexto
@st.dialog("Editar contexto", width="large")
def editar_contexto():
    
    # Define o valor inicial do campo de texto
    if sst.contexto_atual is None:
        valor_inicial = ""
    else:
        valor_inicial = sst.contexto_atual

    # Estrutura da caixa de diálogo
    input = st.text_area("Edite o contexto no campo abaixo:",
                            label_visibility = "collapsed",
                            height=700,
                            value = sst.contexto_atual)
    
    # Botão de salvar alterações
    with st.container(horizontal=True):
        st.space(size="stretch")
        if st.button("Salvar alterações", type="primary"):
            projeto_id = int(sst.projeto_atual.name)
            sst.db.adicionar_contexto(projeto_id, input)
            sst.contexto_atual = sst.db.obter_ultimo_contexto(projeto_id)
            ui.adicionar_mensagem("Contexto editado com sucesso!")
            st.rerun()


# Diálogo de restauração de contexto
@st.dialog("Restaurar contexto", width="large")
def restaurar_contexto():

    # Recupera os contextos do projeto atual
    projeto_id = int(sst.projeto_atual.name)
    contextos = sst.db.listar_contextos(projeto_id)
    contextos.sort_values(by='versao', ascending=False, inplace=True)

    # Define o contexto visualizado inicialmente
    if sst.contexto_visualizado is None:
        sst.contexto_visualizado = contextos.iloc[0]

    # Estrutura da caixa de diálogo
    container = st.container(width="stretch", height=700, border=False)
    col1, col2 = container.columns([1, 4])

    # Lista de contextos disponíveis
    with col1:  
        st.write("### Contextos disponíveis")
        with st.container(height=650, border=False):
            for i in contextos.index:
                versao = contextos.loc[i, 'versao']
                data_hora = contextos.loc[i, 'data_criacao']
                if st.button(f"Versão {versao} ({data_hora})", width="stretch"):
                    sst.contexto_visualizado = contextos.loc[i]

    with col2:
        with st.container(border=True):
            
            # Cabeçalho do contexto selecionado
            versao = sst.contexto_visualizado['versao']
            data_hora = sst.contexto_visualizado['data_criacao']
            st.markdown(f"## Versão {versao} ({data_hora})")

            # Botão de restauração
            if st.button("Restaurar esta versão", type="primary"):
                sst.db.adicionar_contexto(projeto_id, sst.contexto_visualizado['contexto'])
                sst.contexto_atual = sst.db.obter_ultimo_contexto(projeto_id)
                ui.adicionar_mensagem("Contexto restaurado com sucesso!")
                st.rerun()

            # Conteúdo do contexto selecionado
            st.markdown("---")
            with st.container(height=475, border=False):
                st.markdown(sst.contexto_visualizado['contexto'])


# Página de gestão de contexto
st.header(":material/book: Gestão de contexto", divider="gray")

# Mensagens de aviso
if sst.projeto_atual is None:
    st.warning("Nenhum projeto carregado. Por favor, carregue um projeto na seção 'Projetos'.")
elif sst.contexto_atual is None:
    st.info("Nenhum contexto adicionado. Por favor, adicione um contexto para o projeto atual.")

# Visualização do contexto atual
else:    
    md, text = st.tabs(["Markdown", "Texto"])
    with md:
        st.markdown(sst.contexto_atual)
    with text:
        st.code(sst.contexto_atual, language="markdown")

# Botões de ação
st.sidebar.button(":material/wand_stars: Gerar contexto",
                  width="stretch",
                  on_click=gerar_contexto,
                  disabled=sst.projeto_atual is None)
st.sidebar.button(":material/edit: Editar contexto",
                  width="stretch",
                  on_click=editar_contexto,
                  disabled=sst.projeto_atual is None)
st.sidebar.button(":material/restore: Restaurar contexto",
                  width="stretch",
                  on_click=restaurar_contexto,
                  disabled=sst.contexto_atual is None)