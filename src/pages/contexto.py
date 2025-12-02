import streamlit as st

st.write("# :material/book: Gestão de contexto")

# Recuperar contextos do projeto atual
if st.session_state.projeto_atual is not None:
    contextos = st.session_state.db.listar_contextos(st.session_state.projeto_atual.name)


if st.session_state.projeto_atual is None:
    st.warning("Nenhum projeto carregado. Por favor, carregue um projeto na seção 'Projetos'.")
elif st.session_state.contexto_atual is None:
    st.info("Nenhum contexto adicionado. Por favor, adicione um contexto para o projeto atual.")
else:
    
    md, text = st.tabs(["Markdown", "Texto"])
    with md:
        container = st.container(border=True)
        container.markdown(st.session_state.contexto_atual)
    with text:
        st.code(st.session_state.contexto_atual, language="markdown")

