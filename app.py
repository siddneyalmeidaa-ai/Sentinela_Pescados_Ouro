import streamlit as st
import pandas as pd
import random
import plotly.express as px

# CONFIGURAÇÃO KIT RUBI
st.set_page_config(page_title="IA-SENTINELA | Pescados", layout="wide")

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

# BANCO DE DATA PADRÃO OURO
banco = {
    'Salmão':   {'ref': 8.50,  'liberado': 85, 'pendente': 15},
    'Camarão':  {'ref': 13.00, 'liberado': 60, 'pendente': 40},
    'Tilápia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5}
}

# INTERFACE EM ABAS (SEM MENU LATERAL)
aba_config, aba1, aba2 = st.tabs(["⚙️ Configuração", "📊 Dashboard", "📜 Auditoria"])

with aba_config:
    st.subheader("Ajuste de Parâmetros")
    peixe_sel = st.selectbox("Selecione o Pescado:", list(banco.keys()))
    preco_atual = st.number_input("Preço Atual (USD/KG):", value=banco[peixe_sel]['ref'])

dados = banco[peixe_sel]
x_calculado = ((preco_atual - dados['ref']) / dados['ref']) * 100

with aba1:
    st.title(f"🛡️ {peixe_sel}")
    c1, c2 = st.columns(2)
    c1.metric(f"{dados['liberado']}%", "LIBERADO")
    c2.metric(f"{dados['pendente']}%", "PENDENTE")

    st.subheader("📋 Veredito")
    if preco_atual == 1.0:
        st.warning("⚠️ VÁCUO (Zona de Morte)")
        emitir_bip()
        decisao = "pula"
    elif x_calculado >= 10:
        st.error(f"🚫 PULA (Variação: {x_calculado:.2f}%)")
        emitir_bip()
        decisao = "pula"
    else:
        st.success("✅ ENTRA")
        decisao = "entra"

    # Gráfico de Rosca
    fig = px.pie(values=[dados['liberado'], dados['pendente']], 
                 names=['LIBERADO', 'PENDENTE'], hole=0.5,
                 color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig, use_container_width=True)

with aba2:
    st.subheader("📑 Tabela da Favelinha")
    df_favelinha = pd.DataFrame({
        "Rodada": ["Atual"],
        "Projeção": [f"{x_calculado:.2f}%"],
        "Veredito": [decisao]
    })
    st.table(df_favelinha)
    
