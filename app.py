import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP SPA IA SENTINELA - MATRIX REBOOT
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# CSS BLINDADO: MATRIX + VISIBILIDADE DE GRÁFICOS
st.markdown("""
    <style>
        /* Fundo Matrix Suave para não quebrar os gráficos */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
            background-image: url("https://www.psdgraphics.com/wp-content/uploads/2022/01/matrix-code-background.gif");
            background-size: cover;
        }
        
        /* Container das abas com fundo sólido para leitura */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.85) !important;
            border: 1px solid #00FF41;
            padding: 15px;
            border-radius: 5px;
        }

        /* Texto Verde Neon */
        h1, h2, h3, p, span, label {
            color: #00FF41 !important;
            font-family: 'Courier New', Courier, monospace;
        }

        /* Ajuste das Tabs */
        button[data-baseweb="tab"] {
            color: #00FF41 !important;
        }
        
        /* Forçar visibilidade do gráfico */
        .js-plotly-plot {
            background-color: rgba(0,0,0,0) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. BANCO DE DADOS
if 'historico_dia' not in st.session_state:
    st.session_state['historico_dia'] = []

banco = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. INTERFACE OPERACIONAL
tab_relatorio, tab_historia, tab_casado, tab_analisia = st.tabs([
    "📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"
])

with tab_relatorio:
    st.write("### > SPA_IA_SENTINELA_v2.0_")
    item_sel = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    preco_atual = st.number_input(f"VALOR_INPUT (USD):", value=banco[item_sel]['ref'], step=0.1)
    
    dados = banco[item_sel]
    x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
    
    veredito = "PULA" if x_calc >= 10 else "ENTRA"
    cor = "🟢" if veredito == "ENTRA" else "🔴"

    if st.button("🚀 EXEC_AUDITORIA"):
        st.session_state['historico_dia'].insert(0, {
            "Hora": datetime.now().strftime("%H:%M"),
            "Item": item_sel,
            "X%": f"{x_calc:.2f}%",
            "Veredito": veredito
        })
        st.write(f"REGISTRADO: {veredito}")

with tab_analisia:
    st.write(f"### ANÁLISE: {item_sel}")
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{dados['lib']}%")
    c2.metric("PENDENTE", f"{dados['pen']}%")
    
    fig_pizza = px.pie(values=[dados['lib'], dados['pen']], names=['LIBERADO', 'PENDENTE'], 
                 hole=0.6, color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_pizza, use_container_width=True)

with tab_casado:
    st.write("### VISÃO CONSOLIDADA")
    # Tabela
    df_v = pd.DataFrame([{"ITEM": k, "REF": f"${v['ref']:.2f}", "LIB": v['lib'], "PEN": v['pen']} for k, v in banco.items()])
    st.table(df_v)
    
    # Gráfico de Barras Restaurado
    df_g = pd.DataFrame([{"P": k, "S": "LIBERADO", "V": v['lib']} for k, v in banco.items()] + 
                        [{"P": k, "S": "PENDENTE", "V": v['pen']} for k, v in banco.items()])
    
    fig_barra = px.bar(df_g, x="P", y="V", color="S", barmode="stack", 
                       color_discrete_map={"LIBERADO": "#00FF41", "PENDENTE": "#FF0000"})
    fig_barra.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_barra, use_container_width=True)

with tab_historia:
    if st.session_state['historico_dia']:
        st.table(pd.DataFrame(st.session_state['historico_dia']))
    
