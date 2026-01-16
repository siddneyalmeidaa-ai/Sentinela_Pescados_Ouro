import streamlit as st
import pandas as pd
import random
import plotly.express as px

# 1. CONFIGURAÇÃO KIT RUBI
st.set_page_config(page_title="IA-SENTINELA | Pescados", layout="wide")

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

# 2. BANCO DE DADOS (Referência em Dólar e Percentuais)
banco = {
    'Salmão':   {'ref': 8.50,  'liberado': 85, 'pendente': 15},
    'Camarão':  {'ref': 13.00, 'liberado': 60, 'pendente': 40},
    'Tilápia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5}
}

# 3. INTERFACE EM ABAS
aba_config, aba_dashboard, aba_consolidado, aba_auditoria = st.tabs([
    "⚙️ Configuração", 
    "📈 Dashboard Individual", 
    "📊 Visão Consolidada", 
    "📜 Auditoria"
])

with aba_config:
    st.subheader("Ajuste de Parâmetros")
    peixe_sel = st.selectbox("Selecione o Pescado:", list(banco.keys()))
    preco_atual = st.number_input(f"Preço Atual {peixe_sel} (USD/KG):", value=banco[peixe_sel]['ref'])

dados = banco[peixe_sel]
x_calculado = ((preco_atual - dados['ref']) / dados['ref']) * 100

with aba_dashboard:
    st.title(f"🛡️ {peixe_sel}")
    c1, c2 = st.columns(2)
    c1.metric(f"{dados['liberado']}%", "LIBERADO")
    c2.metric(f"{dados['pendente']}%", "PENDENTE")
    
    if preco_atual == 1.0:
        st.warning("⚠️ VEREDITO: VÁCUO")
        emitir_bip()
        decisao = "pula"
    elif x_calculado >= 10:
        st.error(f"🚫 VEREDITO: PULA")
        emitir_bip()
        decisao = "pula"
    else:
        st.success("✅ VEREDITO: ENTRA")
        decisao = "entra"

    fig_ind = px.pie(values=[dados['liberado'], dados['pendente']], 
                     names=['LIBERADO', 'PENDENTE'], hole=0.5,
                     color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig_ind, use_container_width=True)

# --- ABA CONSOLIDADA AJUSTADA (MOEDA E %) ---
with aba_consolidado:
    st.subheader("📊 Resumo de Auditoria Externa (O Casado)")
    
    # Criando os dados formatados
    lista_consolidada = []
    for k, v in banco.items():
        lista_consolidada.append({
            "Pescado": k,
            "Ref. Mercado": f"USD {v['ref']:.2f}",
            "Liberado": f"{v['liberado']}%",
            "Pendente": f"{v['pendente']}%"
        })
    
    df_visual = pd.DataFrame(lista_consolidada)

    # Gráfico de Barras
    df_graph = pd.DataFrame([
        {"Pescado": k, "Status": "Liberado", "Valor": v['liberado']} for k, v in banco.items()
    ] + [
        {"Pescado": k, "Status": "Pendente", "Valor": v['pendente']} for k, v in banco.items()
    ])
    
    fig_cons = px.bar(df_graph, x="Pescado", y="Valor", color="Status",
                      title="Visão Geral do Portfólio (%)",
                      barmode="stack",
                      color_discrete_map={"Liberado": "#2ecc71", "Pendente": "#e74c3c"})
    st.plotly_chart(fig_cons, use_container_width=True)
    
    # Tabela com as correções de Moeda e %
    st.write("**Tabela de Referência Sincronizada:**")
    st.table(df_visual)

with aba_auditoria:
    st.subheader("📑 Tabela da Favelinha")
    st.table(pd.DataFrame({"Indicador": ["Produto", "X Atual", "Veredito"], 
                           "Valor": [peixe_sel, f"{x_calculado:.2f}%", decisao.upper()]}))
    
