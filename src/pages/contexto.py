import pandas as pd
import streamlit as st
from datetime import datetime


# Diálogo de restauração de contexto
@st.dialog("Restaurar contexto", width="large")
def restaurar_contexto():

    # Recupera os contextos do projeto atual
    projeto_id = int(st.session_state.projeto_atual.name)
    contextos = st.session_state.db.listar_contextos(projeto_id)
    contextos.sort_values(by='versao', ascending=False, inplace=True)

    # Define o contexto visualizado inicialmente
    st.session_state.contexto_visualizado = contextos.iloc[0]

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
                    st.session_state.contexto_visualizado = contextos.loc[i]

    with col2:
        with st.container(border=True):
            
            # Cabeçalho do contexto selecionado
            versao = st.session_state.contexto_visualizado['versao']
            data_hora = st.session_state.contexto_visualizado['data_criacao']
            st.markdown(f"## Versão {versao} ({data_hora})")

            # Botão de restauração
            if st.button("Restaurar esta versão"):
                st.session_state.db.adicionar_contexto(projeto_id, st.session_state.contexto_visualizado['contexto'])
                st.session_state.contexto_atual = st.session_state.contexto_visualizado['contexto']
                st.session_state.msg_contexto_restaurado = 1
                st.rerun()
            
            # Conteúdo do contexto selecionado
            st.markdown("---")
            with st.container(height=475, border=False):
                st.markdown(st.session_state.contexto_visualizado['contexto'])



# Página de gestão de contexto
st.write("# :material/book: Gestão de contexto")

# Mensagens de status
if st.session_state.msg_contexto_restaurado == 1:
    st.success("Contexto restaurado com sucesso!")
    st.session_state.msg_contexto_restaurado = 0

# Mensagens de aviso
if st.session_state.projeto_atual is None:
    st.warning("Nenhum projeto carregado. Por favor, carregue um projeto na seção 'Projetos'.")
elif st.session_state.contexto_atual is None:
    st.info("Nenhum contexto adicionado. Por favor, adicione um contexto para o projeto atual.")

# Visualização do contexto atual
else:    
    md, text = st.tabs(["Markdown", "Texto"])
    with md:
        st.markdown(st.session_state.contexto_atual)
    with text:
        st.code(st.session_state.contexto_atual, language="markdown")


st.sidebar.button("Restaurar contexto anterior",
                  width="stretch",
                  on_click=restaurar_contexto,
                  disabled=st.session_state.contexto_atual is None)