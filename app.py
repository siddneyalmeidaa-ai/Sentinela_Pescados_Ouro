import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP SPA IA SENTINELA - MATRIX EDITION
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# CSS PARA CHUVA MATRIX E VISIBILIDADE DAS ABAS
st.markdown("""
    <style>
        /* Efeito Matrix no Fundo */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.9)),
            url("https://mgmpt.com/assets/images/matrix-code.gif");
            background-size: cover;
            color: #00FF41;
        }

        /* Garante que o conteúdo das abas apareça */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #00FF41;
        }

        /* Estilo das Abas (Tabs) */
        button[data-baseweb="tab"] {
            color: #00FF41 !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }

        /* Títulos e Textos */
        h1, h2, h3, p, span {
            color: #00FF41 !important;
            text-shadow: 0 0 5px #00FF41;
        }

        /* Input de números e Selectbox */
        div[data-baseweb="select"], div[data-baseweb="input"] {
            background-color: #111 !important;
            color: #00FF41 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. BANCO DE DADOS ATUALIZADO (ITEM / REF / PENDENTE)
if 'historico_dia' not in st.session_state:
    st.session_state['historico_dia'] = []

banco = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. INTERFACE COM AS ABAS CORRIGIDAS
tab_relatorio, tab_historia, tab_casado, tab_analisia = st.tabs([
    "📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"
])

with tab_relatorio:
    st.write("### > SPA_IA_SENTINELA_v2.0_")
    item_sel = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    preco_atual = st.number_input(f"VALOR_INPUT (USD):", value=banco[item_sel]['ref'], step=0.10)
    
    dados = banco[item_sel]
    x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
    
    veredito = "PULA" if x_calc >= 10 else "ENTRA"
    cor = "🔴" if veredito == "PULA" else "🟢"

    if st.button("🚀 EXEC_AUDITORIA"):
        st.session_state['historico_dia'].insert(0, {
            "Hora": datetime.now().strftime("%H:%M"),
            "Item": item_sel,
            "X%": f"{x_calc:.2f}%",
            "Veredito": veredito
        })
        st.success(f"REGISTRADO: {veredito}")

with tab_analisia:
    st.caption(f"🛡️ ANALISIA DE RISCO: {item_sel}")
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{dados['lib']}%")
    c2.metric("PENDENTE", f"{dados['pen']}%")
    
    st.markdown(f"## VEREDITO: {cor} **{veredito}**")
    
    fig = px.pie(values=[dados['lib'], dados['pen']], names=['LIBERADO', 'PENDENTE'], 
                 hole=0.6, color_discrete_sequence=['#00FF41', '#FF0000'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig, use_container_width=True)

with tab_casado:
    df_v = pd.DataFrame([{"ITEM": k, "REF": f"${v['ref']:.2f}", "LIB": f"{v['lib']}%", "PEN": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_v)

with tab_historia:
    if st.session_state['historico_dia']:
        st.table(pd.DataFrame(st.session_state['historico_dia']))
    else:
        st.write("AGUARDANDO DADOS...")

