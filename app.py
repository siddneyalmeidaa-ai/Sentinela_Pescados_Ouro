import streamlit as st
import pandas as pd
import random
import plotly.express as px

# 1. CONFIGURAÇÃO KIT RUBI - PADRÃO OURO
st.set_page_config(page_title="IA-SENTINELA | Pescados", layout="wide")

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

# 2. BANCO DE DADOS E SINCRONIA
banco = {
    'Salmão':   {'ref': 8.50,  'liberado': 85, 'pendente': 15, 'ncm': '0302.14.00'},
    'Camarão':  {'ref': 13.00, 'liberado': 60, 'pendente': 40, 'ncm': '0306.17.10'},
    'Tilápia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5,  'ncm': '0304.61.00'}
}

with st.sidebar:
    st.header("⚙️ Configuração")
    peixe_sel = st.selectbox("Selecione o Pescado:", list(banco.keys()))
    preco_atual = st.number_input("Preço Atual (USD/KG):", value=banco[peixe_sel]['ref'])

dados = banco[peixe_sel]
x_calculado = ((preco_atual - dados['ref']) / dados['ref']) * 100

# 3. INTERFACE EM ABAS
aba1, aba2 = st.tabs(["📊 Dashboard Operacional", "📜 Histórico e Auditoria"])

with aba1:
    st.title(f"🛡️ Painel {peixe_sel}")
    
    # Métricas Sincronizadas
    c1, c2, c3 = st.columns(3)
    c1.metric(f"LIBERADO", f"{dados['liberado']}%")
    c2.metric(f"PENDENTE", f"{dados['pendente']}%")
    c3.metric("VARIAÇÃO (X)", f"{x_calculado:.2f}%")

    # Ação Imediata e Bip
    st.subheader("📋 Ação Imediata")
    if preco_atual == 1.0:
        st.warning("⚠️ VEREDITO: VÁCUO (Zona de Morte)")
        emitir_bip()
        decisao = "VÁCUO"
    elif x_calculado >= 10:
        st.error(f"🚫 VEREDITO: PULA")
        emitir_bip()
        decisao = "PULA"
    else:
        st.success(f"✅ VEREDITO: ENTRA")
        decisao = "ENTRA"

    # Gráfico de Rosca (Sincronizado)
    df_grafico = pd.DataFrame({
        "Status": [f"LIBERADO {peixe_sel}", f"PENDENTE {peixe_sel}"],
        "Percentual": [dados['liberado'], dados['pendente']]
    })
    fig = px.pie(df_grafico, values='Percentual', names='Status', hole=0.5, 
                 color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig, use_container_width=True)

with aba2:
    st.subheader("📑 Tabela da Favelinha")
    # Tabela Fixa conforme solicitado
    favelinha_data = {
        "Indicador": ["Projeção Rodada", "Status X", "Fator Crítico"],
        "Valor": [f"{random.randint(-5, 12)}%", decisao, "IA-SENTINELA"]
    }
    st.table(pd.DataFrame(favelinha_data))
    
    # Download sem erro de acento no celular
    csv = pd.DataFrame([{"Produto": peixe_sel, "Status": decisao}]).to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 Baixar Auditoria (Excel)", csv, f"auditoria_{peixe_sel}.csv", "text/csv")
    
