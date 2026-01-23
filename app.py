import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. SETUP DE SOBERANIA
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX V4 - CORTINA TOTAL (INJETADA NO FUNDO)
matrix_v4 = """
<div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: black;">
    <canvas id="c"></canvas>
</div>
<script>
    var c = document.getElementById("c");
    var ctx = c.getContext("2d");
    c.height = window.innerHeight;
    c.width = window.innerWidth;
    var matrix = "0101010101ABCDEFHIJKLMNOPQRSTUVWXYZ@#$%&*";
    matrix = matrix.split("");
    var font_size = 14;
    var columns = c.width/font_size;
    var drops = [];
    for(var x = 0; x < columns; x++) drops[x] = 1; 
    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.04)";
        ctx.fillRect(0, 0, c.width, c.height);
        ctx.fillStyle = "#0F0";
        ctx.font = font_size + "px arial";
        for(var i = 0; i < drops.length; i++) {
            var text = matrix[Math.floor(Math.random()*matrix.length)];
            ctx.fillText(text, i*font_size, drops[i]*font_size);
            if(drops[i]*font_size > c.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 35);
</script>
"""
components.html(matrix_v4, height=0)

# 3. CSS DE ALINHAMENTO E BLINDAGEM DE TABELAS
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00FF41;
            border-radius: 10px;
            padding: 15px;
        }
        /* CORREÇÃO DAS TABELAS: LARGURA FIXA E SEM QUEBRA */
        .stTable td, .stTable th {
            white-space: nowrap !important;
            text-align: center !important;
            color: #00FF41 !important;
            font-family: 'Courier New', monospace;
            padding: 12px !important;
        }
        /* CENTRALIZAÇÃO DE MÉTRICAS E TÍTULOS */
        h1, h2, h3, p, label, [data-testid="stMetricValue"] {
            color: #00FF41 !important;
            text-shadow: 0 0 10px #00FF41;
            text-align: center !important;
        }
        .stSelectbox label { text-align: left !important; }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO DE DADOS
if 'logs_finais' not in st.session_state:
    st.session_state['logs_finais'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. INTERFACE OPERACIONAL
t_rel, t_hist, t_casado, t_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with t_rel:
    st.write("### > ACESSO_AO_TERMINAL_")
    item = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    val_at = st.number_input("VALOR_ATUAL ($):", value=banco[item]['ref'], format="%.2f")
    
    # Cálculo com regra S.A.
    variacao = ((val_at - banco[item]['ref']) / banco[item]['ref']) * 100
    veredito = "ENTRA" if variacao < 10 else "PULA"

    if st.button("🚀 REGISTRAR NO SISTEMA"):
        st.session_state['logs_finais'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR": f"$ {val_at:.2f}",
            "X%": f"{variacao:.2f}%",
            "STATUS": veredito
        })
        st.success(f"DADO COMPUTADO: {veredito}")

with t_hist:
    st.write("### > BANCO_DE_DADOS_HISTORICO_")
    if st.session_state['logs_finais']:
        st.table(pd.DataFrame(st.session_state['logs_finais']))
    else:
        st.info("AGUARDANDO INPUTS...")

with t_casado:
    st.write("### > VISÃO_CONSOLIDADA_S.A._")
    # Tabela corrigida
    df_c = pd.DataFrame([{"ITEM": k, "REF": f"$ {v['ref']:.2f}", "LIBERADO": f"{v['lib']}%", "PENDENTE": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_c)
    
    # Gráfico de Barras Corrigido (Fixando Eixo e Dados)
    df_plot = pd.DataFrame([{"ITEM": k, "TIPO": "LIBERADO", "VALOR": v['lib']} for k, v in banco.items()] + 
                           [{"ITEM": k, "TIPO": "PENDENTE", "VALOR": v['pen']} for k, v in banco.items()])
    
    fig_b = px.bar(df_plot, x="ITEM", y="VALOR", color="TIPO", barmode="stack",
                   color_discrete_map={"LIBERADO": "#00FF41", "PENDENTE": "#FF0000"})
    fig_b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color
    
