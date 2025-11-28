import streamlit as st

st.write("# :material/folder_open: Projetos")

st.write("---")
st.write("### Projetos registrados")

# Exibição da lista de projetos
projetos = st.session_state.db.listar_projetos()


if projetos.empty:
    st.write("Nenhum projeto registrado.")
else:
    st.dataframe(projetos)
    


st.write("---")