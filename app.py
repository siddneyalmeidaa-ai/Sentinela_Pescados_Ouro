import streamlit as st
import pandas as pd
import random
import plotly.express as px

# 1. CONFIGURAÇÃO KIT RUBI - PADRÃO OURO
st.set_page_config(page_title="IA-SENTINELA | Pescados", layout="wide")

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

# 2. BANCO DE DADOS SINCRONIZADO
banco = {
    'Salmão':   {'ref': 8.50,  'liberado': 85, 'pendente': 15},
    'Camarão':  {'ref': 13.00, 'liberado': 60, 'pendente': 40},
    'Tilápia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5}
}

# 3. INTERFACE EM ABAS (SEM MENU LATERAL)
aba_config, aba_dashboard, aba_consolidado, aba_auditoria = st.tabs([
    "⚙️ Configuração", 
    "📈 Dashboard Individual", 
    "📊 Visão Consolidada", 
    "📜 Auditoria"
])

# --- ABA: CONFIGURAÇÃO ---
with aba_config:
    st.subheader("Ajuste de Parâmetros Operacionais")
    peixe_sel = st.selectbox("Selecione o Pescado para análise individual:", list(banco.keys()))
    preco_atual = st.number_input(f"Preço Atual do {peixe_sel} (USD/KG):", value=banco[peixe_sel]['ref'])

# Cálculos Individuais
dados = banco[peixe_sel]
x_calculado = ((preco_atual - dados['ref']) / dados['ref']) * 100

# --- ABA: DASHBOARD INDIVIDUAL ---
with aba_dashboard:
    st.title(f"🛡️ Sentinela: {peixe_sel}")
    
    col1, col2 = st.columns(2)
    col1.metric("LIBERADO", f"{dados['liberado']}%")
    col2.metric("PENDENTE", f"{dados['pendente']}%")

    if preco_atual == 1.0:
        st.warning("⚠️ VEREDITO: VÁCUO (Zona de Morte)")
        emitir_bip()
        decisao = "pula"
    elif x_calculado >= 10:
        st.error(f"🚫 VEREDITO: PULA (X: {x_calculado:.2f}%)")
        emitir_bip()
        decisao = "pula"
    else:
        st.success("✅ VEREDITO: ENTRA")
        decisao = "entra"

    # Gráfico de Rosca Individual
    fig_ind = px.pie(values=[dados['liberado'], dados['pendente']], 
                     names=['LIBERADO', 'PENDENTE'], hole=0.5,
                     title=f"Distribuição {peixe_sel}",
                     color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig_ind, use_container_width=True)

# --- ABA: VISÃO CONSOLIDADA (O CASADO) ---
with aba_consolidado:
    st.subheader("📊 Comparativo Consolidado de Pescados")
    
    # Criando tabela para o gráfico de barras
    df_cons = pd.DataFrame([
        {"Pescado": k, "Liberado": v['liberado'], "Pendente": v['pendente']} 
        for k, v in banco.items()
    ])
    
    # Gráfico de Barras Empilhadas (Consolidado)
    fig_cons = px.bar(df_cons, x="Pescado", y=["Liberado", "Pendente"], 
                      title="Visão Geral do Portfólio (%)",
                      barmode="stack",
                      color_discrete_map={"Liberado": "#2ecc71", "Pendente": "#e74c3c"})
    st.plotly_chart(fig_cons, use_container_width=True)
    
    st.write("**Resumo de Auditoria Externa:**")
    st.table(df_cons)

# --- ABA: AUDITORIA ---
with aba_auditoria:
    st.subheader("📑 Tabela da Favelinha")
    df_favelinha = pd.DataFrame({
        "Indicador": ["Produto Selecionado", "Veredito Atual", "Variação Projeção (X)"],
        "Valor": [peixe_sel, decisao.upper(), f"{x_calculado:.2f}%"]
    })
    st.table(df_favelinha)
    
    # Botão de download configurado para celular (UTF-8-SIG evita erro de acento)
    csv = df_favelinha.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 Baixar Auditoria", csv, "auditoria_sentinela.csv", "text/csv")
    
