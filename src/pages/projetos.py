# Importações
import streamlit as st


# Recupera a lista de projetos do banco de dados
projetos = st.session_state.db.listar_projetos()


# Diálogo de criação de projetos
@st.dialog("Adicionar projeto")
def adicionar_projeto():

    # Campos do formulário
    nome = st.text_input("Nome:", placeholder="Obrigatório")
    cliente = st.text_input("Cliente:", placeholder="Obrigatório")
    descricao = st.text_input("Descrição:", placeholder="Opcional")
    
    # Botão de criação
    if st.button("Criar"):

        # Validação dos campos
        if nome == "" or cliente == "":
            st.error("Os campos Nome e Cliente são obrigatórios.")
        
        # Inserção no banco de dados
        else:
            st.session_state.db.adicionar_projeto(nome, cliente, descricao)
            st.rerun()


# Carregamento de projetos
@st.dialog("Carregar projeto")
def carregar_projeto():

    # Seleção do projeto
    id_projeto = st.selectbox("Selecione o projeto para carregar:",
                              options=projetos.index.tolist(),
                              format_func=lambda x: projetos.loc[x, 'nome'])
    
    # Botão de carregamento
    if st.button("Carregar", width="stretch"):
        st.session_state.projeto_atual = projetos.loc[id_projeto]
        st.rerun()


# Elementos da página
st.write("# :material/folder_open: Projetos")

if projetos.empty:
    st.write("Nenhum projeto registrado.")
else:
    config = {
        "_index": st.column_config.NumberColumn("ID"),
        "nome": st.column_config.TextColumn("Nome"),
        "cliente": st.column_config.TextColumn("Cliente"),
        "descricao": st.column_config.TextColumn("Descrição", width="large")
    }
    st.dataframe(projetos, column_config=config, width="stretch")

st.sidebar.button(":material/add: Adicionar projeto",
                  width="stretch",
                  on_click=adicionar_projeto)
st.sidebar.button(":material/upload: Carregar projeto", 
                  width="stretch",
                  disabled=projetos.empty,
                  on_click=carregar_projeto)