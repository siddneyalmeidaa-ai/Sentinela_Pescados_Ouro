import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP MATRIX - S.P.A.
st.set_page_config(
    page_title="SENTINELA MATRIX", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# DESIGN MATRIX - O PADRÃO SOBERANO
st.markdown("""
    <style>
        /* Fundo Preto Absoluto e Fonte Verde Matrix */
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #000000;
            color: #00FF41;
            font-family: 'Courier Prime', monospace;
        }

        /* Ocultar elementos padrão */
        [data-testid="stHeader"] {visibility: hidden; height: 0px;}
        footer {display:none !important;}
        
        /* Estilização de Métricas */
        [data-testid="stMetricValue"] {
            color: #00FF41 !important;
            text-shadow: 0 0 10px #00FF41;
            font-size: 2.5rem !important;
        }
        [data-testid="stMetricLabel"] {
            color: #00FF41 !important;
            letter-spacing: 2px;
        }

        /* Botão S.P.A. Estilo Terminal */
        .stButton>button {
            background-color: #000000;
            color: #00FF41;
            border: 2px solid #00FF41;
            border-radius: 0px;
            width: 100%;
            height: 3em;
            font-weight: bold;
            text-transform: uppercase;
            box-shadow: 0 0 15px #00FF41;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #00FF41;
            color: #000000;
        }

        /* Tabs Matrix */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #000000;
        }
        .stTabs [data-baseweb="tab"] {
            color: #00FF41 !important;
        }

        /* Tabelas Matrix */
        .stDataFrame, div[data-testid="stTable"] {
            border: 1px solid #00FF41;
        }
    </style>
""", unsafe_allow_html=True)

# 2. BANCO DE DADOS - PADRÃO OURO
banco = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. INTERFACE OPERACIONAL
aba_ajuste, aba_dash, aba_casado, aba_hist = st.tabs([
    "📟 TERMINAL", "📈 MATRIX_DASH", "📊 CONSOLIDADO", "📂 REGISTROS"
])

with aba_ajuste:
    st.write("### > SPA_IA_SENTINELA_v2.0_")
    item_sel = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    preco_atual = st.number_input(f"VALOR_INPUT (USD):", value=banco[item_sel]['ref'], step=0.10)
    
    dados = banco[item_sel]
    x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
    
    if x_calc >= 10: 
        veredito = "PULA"; cor = "🟡"
    else: 
        veredito = "ENTRA"; cor = "🟢"

    if st.button("EXEC_AUDITORIA"):
        st.session_state.setdefault('historico_dia', []).insert(0, {
            "Hora": datetime.now().strftime("%H:%M"),
            "Item": item_sel,
            "Variação": f"{x_calc:.2f}%",
            "Veredito": veredito
        })
        st.toast(f"LOG_REGISTRADO: {veredito}")

with aba_dash:
    st.caption(f"STATUS_REPORT: {item_sel}")
    
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{dados['lib']}%")
    c2.metric("PENDENTE", f"{dados['pen']}%")
    
    st.markdown(f"### VEREDITO: {cor} {veredito}")
    
    # Gráfico Matrix Colors
    fig_ind = px.pie(
        values=[dados['lib'], dados['pen']], 
        names=['LIBERADO', 'PENDENTE'], 
        hole=0.6,
        color_discrete_sequence=['#00FF41', '#FF0000']
    )
    fig_ind.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#00FF41",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_ind, use_container_width=True, config={'displayModeBar': False})

with aba_casado:
    st.caption("VISÃO_ESTRUTURAL_PEIXES")
    df_v = pd.DataFrame([{"ITEM": k, "REF": f"${v['ref']:.2f}", "LIB": f"{v['lib']}%", "PEN": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_v)

with aba_hist:
    st.caption("LOG_SISTEMA_AUDITORIA")
    if 'historico_dia' in st.session_state and st.session_state['historico_dia']:
        st.table(pd.DataFrame(st.session_state['historico_dia']))
        
