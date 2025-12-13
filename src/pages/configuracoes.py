import streamlit as st
from streamlit import session_state as sst
import src.utils.ui as ui

st.header(":material/settings: Configurações", divider="gray")


# Integração com IA Generativa
st.subheader("Integração com IA Generativa")

if 'ai' in sst:
    ai = sst.ai
    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        # Define placeholder e valor padrão
        # tem_chave = ai.api_key and ai.api_key.strip() and ai.api_key != "None"
        placeholder_msg = "Chave configurada no sistema (só sobrescreva se necessário)" if ai.api_key else "Insira sua Chave API"
        base_url_atual = ai.base_url if ai.base_url else "https://api.openai.com/v1"

        novo_api_key = col1.text_input("Chave API (API Key)", value="", type="password", placeholder=placeholder_msg)
        novo_base_url = col2.text_input("Endereço API (Base URL)", value=base_url_atual)

        if st.button("Salvar Configurações", type="primary"):
            if not novo_api_key or not novo_base_url:
                st.warning("Preencha os campos acima para salvar.")
            else:
                with st.spinner("Salvando configurações no sistema..."):
                    ai.save_config(novo_api_key, novo_base_url)
                    ui.adicionar_mensagem("Credenciais de IA salvas com sucesso!")
                    st.rerun()
else:
    st.error("Erro: Módulo de IA não inicializado na sessão.")