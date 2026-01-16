import streamlit as st
import pandas as pd
import random

# CONFIGURAÇÃO KIT RUBI
st.set_page_config(page_title="IA-SENTINELA | Pescados", layout="wide")

# FUNÇÃO PARA O BIP (Sinal Sonoro)
def emitir_bip():
    # Gera um som de alerta via HTML
    bip_html = """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.components.v1.html(bip_html, height=0)

# 1. BANCO DE DADOS SINCRONIZADO
banco_pescados = {
    'Salmão':   {'ref': 8.50,  'liberado': 85, 'pendente': 15, 'ncm': '0302.14.00'},
    'Camarão':  {'ref': 13.00, 'liberado': 60, 'pendente': 40, 'ncm': '0306.17.10'},
    'Tilápia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5,  'ncm': '0304.61.00'}
}

st.title("🛡️ Painel de Inteligência com Alerta Sonoro")

with st.sidebar:
    peixe_sel = st.selectbox("Selecione o Pescado:", list(banco_pescados.keys()))
    preco_atual = st.number_input("Preço Atual (USD/KG):", value=banco_pescados[peixe_sel]['ref'])

dados = banco_pescados[peixe_sel]
x_calculado = ((preco_atual - dados['ref']) / dados['ref']) * 100

# 2. VEREDITO COM SINALIZAÇÃO POR BIP
st.subheader("📋 Ação Imediata")

if preco_atual == 1.0: # Regra do Vácuo
    st.warning("⚠️ VEREDITO: VÁCUO (Zona de Morte)")
    emitir_bip() # <--- BIP AQUI
    decisao = "VÁCUO"
elif x_calculado >= 10:
    st.error(f"🚫 VEREDITO: PULA (Alta de {x_calculado:.2f}%)")
    emitir_bip() # <--- BIP AQUI
    decisao = "PULA"
else:
    st.success(f"✅ VEREDITO: ENTRA (Normalidade)")
    decisao = "ENTRA"

# 3. MÉTRICAS SINCRONIZADAS
col1, col2 = st.columns(2)
col1.metric(f"LIBERADO {peixe_sel}", f"{dados['liberado']}%")
col2.metric(f"PENDENTE {peixe_sel}", f"{dados['pendente']}%")
