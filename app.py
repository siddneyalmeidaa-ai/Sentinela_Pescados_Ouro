import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP SPA IA SENTINELA - S.P.A.
st.set_page_config(
    page_title="SPA IA SENTINELA", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# CSS PARA OCULTAÇÃO TOTAL (HEADER, FOOTER E MENUS)
st.markdown("""
    <style>
        [data-testid="stHeader"] {visibility: hidden; height: 0px;}
        [data-testid="stSidebar"] {display: none;}
        footer {display:none !important;}
        .stActionButton {display: none;} 
        [data-testid="stStatusWidget"] {display: none;}
        div[data-testid="stDecoration"] {display:none;}
        .block-container {padding-top: 0rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

if 'historico_dia' not in st.session_state:
    st.session_state['historico_dia'] = []

# 2. BANCO DE DADOS
banco = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. INTERFACE SPA
aba_ajuste, aba_dash, aba_casado, aba_hist = st.tabs([
    "⚙️ Ajuste", "📈 Dash", "📊 Casado", "📂 Hist"
])

with aba_ajuste:
    st.write("### SPA IA SENTINELA")
    peixe_sel = st.selectbox("Selecione o Item:", list(banco.keys()))
    preco_atual = st.number_input(f"Preço Atual (USD):", value=banco[peixe_sel]['ref'], step=0.10)
    
    dados = banco[peixe_sel]
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
        st.toast(f"Registrado: {veredito}")

with aba_dash:
    st.caption(f"🛡️ Dash Individual: {peixe_sel}")
    if preco_atual == 1.0 or x_calc >= 10: emitir_bip()
    
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{dados['lib']}%")
    c2.metric("PENDENTE", f"{dados['pen']}%")
    
    st.markdown(f"### Veredito: {cor} **{veredito}**")
    
    # CORREÇÃO DEFINITIVA DA LEGENDA NO GRÁFICO PIZZA
    fig_ind = px.pie(
        values=[dados['lib'], dados['pen']], 
        names=['LIBERADO', 'PENDENTE'], 
        hole=0.6,
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    fig_ind.update_layout(
        margin=dict(t=10, b=10, l=10, r=10), 
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.1, 
            xanchor="center", 
            x=0.5,
            font=dict(size=14) # Garante que a fonte seja legível e não corte
        )
    )
    st.plotly_chart(fig_ind, use_container_width=True, config={'displayModeBar': False})

with aba_casado:
    st.caption("📊 Visão Consolidada")
    df_v = pd.DataFrame([{"P": k, "Ref": f"${v['ref']:.2f}", "Lib": f"{v['lib']}%", "Pen": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_v)
    
    df_g = pd.DataFrame([{"P": k, "S": "LIBERADO", "V": v['lib']} for k, v in banco.items()] + 
                        [{"P": k, "S": "PENDENTE", "V": v['pen']} for k, v in banco.items()])
    fig_c = px.bar(df_g, x="P", y="V", color="S", barmode="stack", 
                   color_discrete_map={"LIBERADO": "#2ecc71", "PENDENTE": "#e74c3c"}, height=300)
    fig_c.update_layout(xaxis_title="", yaxis_title="", showlegend=True)
    st.plotly_chart(fig_c, use_container_width=True, config={'displayModeBar': False})

with aba_hist:
    st.caption("📂 Histórico")
    if st.session_state['historico_dia']:
        df_r = pd.DataFrame(st.session_state['historico_dia'])
        st.table(df_r)
        csv = df_r.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 Baixar CSV S.P.A.", csv, "auditoria_spa.csv", "text/csv")
        
