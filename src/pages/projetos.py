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
    if st.button("Criar", width="stretch"):

        # Validação dos campos
        if nome == "" or cliente == "":
            st.error("Os campos Nome e Cliente são obrigatórios.")
        
        # Inserção no banco de dados
        else:
            st.session_state.db.adicionar_projeto(nome, cliente, descricao)
            st.session_state.msg_projeto_criado = 1
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
        
        # Definição do projeto atual na sessão
        st.session_state.projeto_atual = projetos.loc[id_projeto]
        st.session_state.contexto_atual = st.session_state.db.obter_ultimo_contexto(id_projeto)
        st.session_state.contexto_visualizado = None
        
        # Mensagem de sucesso
        st.session_state.msg_projeto_carregado = 1
        st.rerun()


# Deletar projetos
@st.dialog("Deletar projeto")
def deletar_projeto():

    # Seleção do projeto
    id_projeto = st.selectbox("Selecione o projeto para deletar:",
                              options=projetos.index.tolist(),
                              format_func=lambda x: projetos.loc[x, 'nome'])
    
    st.text("Se deseja realmente deletar o projeto, escreva no campo abaixo:")
    st.markdown(f":red[**Deletar completamente projeto {projetos.loc[id_projeto, 'nome']}**]")
    texto = st.text_input(label="Confirmação de deleção:")

    # Botão de deleção
    if st.button("Deletar", width="stretch", type="primary"):
        if texto == f"Deletar completamente projeto {projetos.loc[id_projeto, 'nome']}":
            st.session_state.db.deletar_projeto(id_projeto)
            st.session_state.msg_projeto_deletado = 1
            try:
                if st.session_state.projeto_atual.name == id_projeto:
                    st.session_state.projeto_atual = None
                    st.session_state.contexto_atual = None
                    st.session_state.contexto_visualizado = None
            except: pass
            st.rerun()
        else:
            st.error("Texto incorreto. Operação de deleção cancelada.")


# Cabeçalho da página
st.write("# :material/folder_open: Projetos")


# Mensagens de status
if st.session_state.msg_projeto_criado == 1:
    st.success("Projeto criado com sucesso!")
    st.session_state.msg_projeto_criado = 0
if st.session_state.msg_projeto_carregado == 1:
    st.success("Projeto carregado com sucesso!")
    st.session_state.msg_projeto_carregado = 0
if st.session_state.msg_projeto_deletado == 1:
    st.success("Projeto deletado com sucesso!")
    st.session_state.msg_projeto_deletado = 0


# Conteúdo da página
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
st.sidebar.button(":material/delete: Deletar projeto",
                  width="stretch",
                  disabled=projetos.empty,
                  on_click=deletar_projeto)