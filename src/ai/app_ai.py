import os
import subprocess
import streamlit as st
from langchain_openai import ChatOpenAI

class AppAI:
    def __init__(self):
        # Tenta carregar as variáveis de ambiente diretamente; 
        # se elas foram definidas na sessão atual via save_config, elas estarão no os.environ
        self.api_key = os.environ.get("APP_AI_API_KEY")
        self.base_url = os.environ.get("APP_AI_BASE_URL", "https://api.openai.com/v1")

    def save_config(self, api_key: str, base_url: str):
        """
        Salva as configurações nas variáveis de ambiente do sistema (Windows)
        e atualiza o processo atual para uso imediato.
        """

        # 1. Atualizar sessão atual (runtime)
        os.environ["APP_AI_API_KEY"] = api_key
        os.environ["APP_AI_BASE_URL"] = base_url
        
        # Atualiza os atributos da instância
        self.api_key = api_key
        self.base_url = base_url

        # 2. Persistir no sistema (Windows) usando setx
        # setx grava no registro do usuário, disponível para futuros processos
        subprocess.run(["setx", "APP_AI_API_KEY", api_key], check=True, shell=True)
        subprocess.run(["setx", "APP_AI_BASE_URL", base_url], check=True, shell=True)
            

    def get_llm(self, temperature=0.7, model="gpt-3.5-turbo"):
        """
        Retorna uma instância configurada do LangChain ChatOpenAI.
        """
        if not self.api_key:
            return None
            
        return ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=model,
            temperature=temperature
        )
