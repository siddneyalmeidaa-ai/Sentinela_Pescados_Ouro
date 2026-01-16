import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. CONFIGURAÇÃO KIT RUBI
st.set_page_config(page_title="IA-SENTINELA | Auditoria", layout="wide")

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

if 'historico_dia' not in st.session_state:
    st.session_state['historico_dia'] = []

# 2. BANCO DE DADOS PADRÃO OURO
banco = {
    'Salmão':   {'ref': 8.50,  'liberado': 85, 'pendente': 15},
    'Camarão':  {'ref': 13.00, 'liberado': 60, 'pendente': 40},
    'Tilápia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5}
}

# 3. INTERFACE EM ABAS (ESTRUTURA COMPLETA)
aba_config, aba_dashboard, aba_consolidado, aba_relatorio = st.tabs([
    "⚙️ Configuração", "📈 Dashboard Individual", "📊 Visão Consolidada", "📂 Relatórios do Dia"
])

with aba_config:
    st.subheader("Entrada de Dados")
    peixe_sel = st.selectbox("Selecione o Pescado:", list(banco.keys()))
    preco_atual = st.number_input(f"Preço Atual {peixe_sel} (USD/KG):", value=banco[peixe_sel]['ref'])
    
    # Cálculos em tempo real para os gráficos não sumirem
    dados = banco[peixe_sel]
    x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
    
    if preco_atual == 1.0: veredito = "VÁCUO"; cor = "🔴"
    elif x_calc >= 10: veredito = "PULA"; cor = "🟡"
    else: veredito = "ENTRA"; cor = "🟢"

    if st.button("🔔 Registrar Aumento no Relatório"):
        st.session_state['historico_dia'].insert(0, {
            "Horário": datetime.now().strftime("%H:%M:%S"),
            "Produto": peixe_sel,
            "Preço": f"USD {preco_atual:.2f}",
            "X": f"{x_calc:.2f}%",
            "Veredito": f"{cor} {veredito}"
        })
        st.success("Histórico atualizado com sucesso!")

with aba_dashboard:
    st.title(f"🛡️ Sentinela: {peixe_sel}")
    if preco_atual == 1.0 or x_calc >= 10: emitir_bip()
    
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{dados['liberado']}%")
    c2.metric("PENDENTE", f"{dados['pendente']}%")
    
    st.info(f"Veredito Atual: {cor} {veredito} (Variação: {x_calc:.2f}%)")
    
    fig_ind = px.pie(values=[dados['liberado'], dados['pendente']], 
                     names=['LIBERADO', 'PENDENTE'], hole=0.5,
                     color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig_ind, use_container_width=True)

with aba_consolidado:
    st.subheader("📊 O Casado (Panorama Geral)")
    # Tabela formatada com Moeda e %
    df_visual = pd.DataFrame([{
        "Pescado": k, "Ref. Mercado": f"USD {v['ref']:.2f}", 
        "Liberado": f"{v['liberado']}%", "Pendente": f"{v['pendente']}%"
    } for k, v in banco.items()])
    st.table(df_visual)
    
    # Gráfico de Barras fixo
    df_cons = pd.DataFrame([{"Pescado": k, "Liberado": v['liberado'], "Pendente": v['pendente']} for k, v in banco.items()])
    fig_cons = px.bar(df_cons, x="Pescado", y=["Liberado", "Pendente"], barmode="stack",
                      color_discrete_map={"Liberado": "#2ecc71", "Pendente": "#e74c3c"})
    st.plotly_chart(fig_cons, use_container_width=True)

with aba_relatorio:
    st.subheader("📂 Base de Relatórios (Histórico do Dia)")
    if st.session_state['historico_dia']:
        st.dataframe(pd.DataFrame(st.session_state['historico_dia']), use_container_width=True)
    else:
        st.warning("Nenhum aumento registrado manualmente ainda.")
        
