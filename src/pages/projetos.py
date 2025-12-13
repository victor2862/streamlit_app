# Importações
import streamlit as st
from streamlit import session_state as sst
import src.utils.ui as ui


# Recupera a lista de projetos do banco de dados
projetos = sst.db.listar_projetos()


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
            sst.db.adicionar_projeto(nome, cliente, descricao)
            ui.adicionar_mensagem("Projeto criado com sucesso!")
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
        sst.projeto_atual = projetos.loc[id_projeto]
        sst.contexto_atual = sst.db.obter_ultimo_contexto(id_projeto)
        sst.contexto_visualizado = None
        
        # Mensagem de sucesso
        ui.adicionar_mensagem("Projeto carregado com sucesso!") 
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
            sst.db.deletar_projeto(id_projeto)
            ui.adicionar_mensagem("Projeto deletado com sucesso!")
            try:
                if sst.projeto_atual.name == id_projeto:
                    sst.projeto_atual = None
                    sst.contexto_atual = None
                    sst.contexto_visualizado = None
            except: pass
            st.rerun()
        else:
            st.error("Texto incorreto. Operação de deleção cancelada.")


# Cabeçalho da página
st.header(":material/folder_open: Projetos", divider="gray")


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


# Botões de ação
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