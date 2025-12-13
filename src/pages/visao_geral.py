import streamlit as st
from streamlit import session_state as sst

st.header(":material/assessment: Visão Geral", divider="gray")

if sst.projeto_atual is None:
    st.warning("Nenhum projeto carregado. Por favor, carregue um projeto na seção 'Projetos'.")
else:
    pass


