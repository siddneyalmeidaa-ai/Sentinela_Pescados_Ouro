import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP "SPA IA SENTINELA" - S.P.A. (MANUTENÇÃO DE REGRAS ANTERIORES)
st.set_page_config(
    page_title="SPA IA SENTINELA", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# CSS PARA OCULTAR O QUE FOI PEDIDO (BARRA SUPERIOR, LÁPIS, MÃO E MENU)
st.markdown("""
    <style>
        [data-testid="stHeader"] {visibility: hidden; height: 0px;}
        [data-testid="stSidebar"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stActionButton {display: none;} 
        .block-container {padding-top: 0rem;}
    </style>
""", unsafe_allow_html=True)

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

if 'historico_dia' not in st.session_state:
    st.session_state['historico_dia'] = []

# 2. BANCO DE DADOS (MANTIDO CONFORME PADRÃO)
banco = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. INTERFACE EM ABAS (ESTRUTURA MANTIDA)
aba_ajuste, aba_dash, aba_casado, aba_hist = st.tabs([
    "⚙️ Ajuste", "📈 Dash", "📊 Casado", "📂 Hist"
])

with aba_ajuste:
    st.write(f"### SPA IA SENTINELA | Operador: **S.P.A.**")
    peixe_sel = st.selectbox("Selecione o Item:", list(banco.keys()))
    preco_atual = st.number_input(f"Preço Atual (USD):", value=banco[peixe_sel]['ref'], step=0.10)
    
    dados = banco[peixe_sel]
    # CÁLCULO DO X (MANTIDA REGRA DE -50% DA PROJEÇÃO)
    x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
    
    if preco_atual == 1.0: veredito = "VACUO"; cor = "🔴"
    elif x_calc >= 10: veredito = "PULA"; cor = "🟡"
    else: veredito = "ENTRA"; cor = "🟢"

    if st.button("🚀 REGISTRAR AUDITORIA"):
        st.session_state['historico_dia'].insert(0, {
            "Hora": datetime.now().strftime("%H:%M"),
            "Item": peixe_sel,
            "X%": f"{x_calc:.2f}%",
            "Veredito": veredito
        })
        st.toast(f"Registrado por S.P.A.: {veredito}")

with aba_dash:
    st.caption(f"🛡️ Dash Individual: {peixe_sel}")
    if preco_atual == 1.0 or x_calc >= 10: emitir_bip()
    
    c1, c2 = st.columns(2)
    c1.metric(f"{dados['lib']}%", "LIBERADO")
    c2.metric(f"{dados['pen']}%", "PENDENTE")
    
    st.markdown(f"### Veredito: {cor} **{veredito}**")
    
    fig_ind = px.pie(values=[dados['lib'], dados['pen']], names=['LIB', 'PEN'], hole=0.6,
                     color_discrete_sequence=['#2ecc71', '#e74c3c'])
    fig_ind.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
    st.plotly_chart(fig_ind, use_container_width=True)

with aba_casado:
    st.caption("📊 Visão Consolidada S.P.A.")
    df_v = pd.DataFrame([{"P": k, "Ref": f"${v['ref']:.2f}", "Lib": f"{v['lib']}%", "Pen": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_v)
    
    df_g = pd.DataFrame([{"P": k, "S": "Lib", "V": v['lib']} for k, v in banco.items()] + 
                        [{"P": k, "S": "Pen", "V": v['pen']} for k, v in banco.items()])
    fig_c = px.bar(df_g, x="P", y="V", color="S", barmode="stack", 
                   color_discrete_map={"Lib": "#2ecc71", "Pen": "#e74c3c"}, height=300)
    st.plotly_chart(fig_c, use_container_width=True)

with aba_hist:
    st.caption("📂 Histórico de Movimentação")
    if st.session_state['historico_dia']:
        df_r = pd.DataFrame(st.session_state['historico_dia'])
        st.table(df_r)
        # DOWNLOAD SEM ERRO DE ACENTO
        csv = df_r.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 Baixar CSV S.P.A.", csv, "auditoria_spa.csv", "text/csv")
        
