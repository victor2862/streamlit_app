import streamlit as st
from streamlit import session_state as sst
import src.utils.ui as ui
import json
import os
from src.utils.ai_utils import modelos_disponiveis


# Diálogo de edição de System Prompt
@st.dialog("Editar System Prompt", width="large")
def editar_system_prompt(agente):
    nome = agente['nome']
    system_prompt_atual = agente['system_prompt'] or ""
    
    st.write(f"Editando prompt do agente: **{nome}**")
    
    novo_prompt = st.text_area("System Prompt", value=system_prompt_atual, height=400)
    
    if st.button("Salvar", type="primary"):
        sst.db.atualizar_agente(nome, system_prompt=novo_prompt)
        ui.adicionar_mensagem(f"System Prompt de '{nome}' atualizado com sucesso!")
        st.rerun()

st.header(":material/settings: Configurações", divider="gray")


# Integração com IA Generativa
st.subheader("Integração com IA Generativa")

if 'ai' in sst:
    ai = sst.ai
    with st.container(border=True, horizontal=True, vertical_alignment="bottom"):
        
        # Define placeholder e valor padrão
        placeholder_msg = "Chave configurada no sistema (só sobrescreva se necessário)" if ai.api_key else "Insira sua Chave API"
        base_url_atual = ai.base_url if ai.base_url else "https://api.openai.com/v1"

        novo_api_key = st.text_input("Chave API (API Key)", value="", type="password", placeholder=placeholder_msg)
        novo_base_url = st.text_input("Endereço API (Base URL)", value=base_url_atual)

        if st.button("Salvar Configurações", type="primary"):
            if not novo_api_key or not novo_base_url:
                st.toast(":material/warning: Preencha os campos acima para salvar.")
            else:
                ai.save_config(novo_api_key, novo_base_url)
                ui.adicionar_mensagem("Credenciais de IA salvas com sucesso!")
                st.rerun()
else:
    st.error("Erro: Módulo de IA não inicializado na sessão.")


# Configuração de Agentes
st.subheader("Configuração de Agentes")

if 'db' in sst:
    # Obter todos os agentes do banco de dados
    df_agentes = sst.db.listar_agentes()

    if not df_agentes.empty:
        
        # Carregar lista de modelos disponíveis
        lista_modelos_padrao = modelos_disponiveis()

        # Renderizar lista de agentes
        with st.container(border=True):
            
            for index, row in df_agentes.iterrows():
                agente = row.to_dict()
                nome_agente = agente['nome']
                
                with st.container(horizontal=True, vertical_alignment="center"):
                    st.markdown(f"**{nome_agente}**")
                    
                    # Duplicar lista de modelos e adicionar modelo atual se não existir
                    modelos_disponiveis = lista_modelos_padrao.copy()
                    modelo_atual = agente['modelo']

                    if modelo_atual not in modelos_disponiveis:
                        modelos_disponiveis.append(modelo_atual)
                    
                    # Caixa de seleção de modelo
                    index_modelo = modelos_disponiveis.index(modelo_atual) if modelo_atual in modelos_disponiveis else 0
                    novo_modelo = st.selectbox(
                        "Modelo", 
                        options=modelos_disponiveis, 
                        index=index_modelo, 
                        key=f"sel_modelo_{nome_agente}",
                        label_visibility="collapsed",
                        width=600
                    )
                    
                    if novo_modelo != modelo_atual:
                        sst.db.atualizar_agente(nome_agente, modelo=novo_modelo)
                        st.toast(f"Modelo do agente '{nome_agente}' atualizado para {novo_modelo}")
                
                    if st.button("Editar Prompt", key=f"btn_edit_{nome_agente}", icon=":material/edit:"):
                        editar_system_prompt(agente)
    else:
        st.info("Nenhum agente encontrado no banco de dados.")

else:
    st.error("Erro: Banco de dados não conectado.")