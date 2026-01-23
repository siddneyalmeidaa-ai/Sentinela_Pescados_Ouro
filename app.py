import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP DE SEGURANÇA
st.set_page_config(page_title="SENTINELA S.A.", layout="wide")

# Inicialização limpa da memória
if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

# Botão para resetar se houver lixo de memória travando a tela
if st.sidebar.button("🧹 LIMPAR MEMÓRIA E ERROS"):
    st.session_state['logs_sentinela'] = []
    st.rerun()

# 2. BANCO DE DADOS PADRÃO OURO
banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. ESTILO CSS (TEXTO SIMPLES PARA NÃO CORTAR NO CELULAR)
st.markdown("<style>.stApp { background-color: #000; color: #00FF41; }</style>", unsafe_allow_html=True)

# 4. SISTEMA DE ABAS
t_term, t_rel, t_analise = st.tabs(["🎮 TERMINAL", "📑 RELATÓRIO", "📊 MÉTRICAS"])

# --- ABA 1: TERMINAL ---
with t_term:
    st.write("### > ENTRADA DE DADOS")
    item_op = st.selectbox("PRODUTO:", list(banco.keys()))
    
    # Stake orientada: valor exato conforme solicitado (Ex: 8.50)
    val_op = st.number_input("VALOR ATUAL ($):", value=banco[item_op]['ref'], step=0.10)
    
    if st.button("🚀 EXECUTAR REGISTRO"):
        # Regra: -50% da projeção na variação
        var_bruta = ((val_op - banco[item_op]['ref']) / banco[item_op]['ref'])
        
        # Salvando com chaves numéricas puras para evitar TypeError
        st.session_state['logs_sentinela'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item_op,
            "VALOR_NUM": float(val_op),
            "STATUS": "ENTRA" if var_bruta < 0.1 else "PULA"
        })
        st.success(f"REGISTRO {item_op} CON
        
