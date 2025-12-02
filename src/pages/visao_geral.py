import streamlit as st

st.write("# :material/assessment: Visão Geral")

if st.session_state.projeto_atual is None:
    st.warning("Nenhum projeto carregado. Por favor, carregue um projeto na seção 'Projetos'.")
else:
    pass


