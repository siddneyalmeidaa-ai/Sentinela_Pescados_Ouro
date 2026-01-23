import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP E LIMPEZA DE MEMÓRIA (ERRO DE CHAVE)
st.set_page_config(page_title="SENTINELA S.A.", layout="wide")

if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

# Função para limpar dados antigos que causam o KeyError
if st.sidebar.button("🧹 RESETAR MEMÓRIA (LIMPAR ERROS)"):
    st.session_state['logs_sentinela'] = []
    st.rerun()

# 2. BANCO PADRÃO OURO
banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. ESTILO VISUAL DIRETO (SEM JAVASCRIPT)
st.markdown("""
    <style>
        .reportview-container { background: #000; }
        .nota-fiscal {
            font-family: 'Courier New', monospace;
            border: 2px dashed #00FF41;
            padding: 15px;
            background-color: rgba(0,20,0,0.9);
            color: #00FF41;
        }
    </style>
""", unsafe_allow_html=True)

# 4. SISTEMA DE ABAS
t_term, t_rel, t_analise = st.tabs(["🎮 TERMINAL", "📑 RELATÓRIO", "📊 MÉTRICAS"])

with t_term:
    st.write("### > ENTRADA DE OPERAÇÃO")
    item_op = st.selectbox("PRODUTO", list(banco.keys()))
    
    # Stake orientada: Valor exato conforme solicitado
    val_op = st.number_input("VALOR ($)", value=banco[item_op]['ref'], step=0.10)
    
    if st.button("🚀 REGISTRAR AGORA"):
        # Cálculo de variação
        var_bruta = ((val_op - banco[item_op]['ref']) / banco[item_op]['ref'])
        # Regra: -50% da projeção aplicada
        projecao = var_bruta * 0.5 
        
        novo_log = {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item_op,
            "VALOR_NUM": float(val_op), # Força ser número puro
            "STATUS": "ENTRA" if var_bruta < 0.1 else "PULA"
        }
        st.session_state['logs_sentinela'].insert(0, novo_log
        
