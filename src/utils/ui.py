import streamlit as st
from streamlit import session_state as sst

def adicionar_mensagem(texto, tipo="success"):
    """
    Adiciona uma mensagem à fila de notificações.
    
    Args:
        texto (str): O texto da mensagem.
        tipo (str): O tipo da mensagem ('success', 'error', 'warning', 'info'). Default: 'success'.
    """
    if 'notificacoes' not in sst:
        sst.notificacoes = []
    sst.notificacoes.append({"texto": texto, "tipo": tipo})

def exibir_mensagens():
    """
    Exibe todas as mensagens na fila de notificações e limpa a fila.
    """
    if 'notificacoes' not in sst:
        return
        
    for msg in sst.notificacoes:
        if msg['tipo'] == 'success':
            st.success(msg['texto'])
        elif msg['tipo'] == 'error':
            st.error(msg['texto'])
        elif msg['tipo'] == 'warning':
            st.warning(msg['texto'])
        else:
            st.info(msg['texto'])
    
    # Limpa as mensagens após exibir
    sst.notificacoes = []
