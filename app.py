import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. COMANDO CENTRAL
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (CÓDIGO FECHADO E SEGURO)
matrix_vFinal = """
<div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: black;">
    <canvas id="m"></canvas>
</div>
<script>
    var c = document.getElementById("m");
    var ctx = c.getContext("2d");
    c.height = window.innerHeight; c.width = window.innerWidth;
    var txt = "0101010101ABCDEFHIJKLMNOPQRSTUVWXYZ@#$%&*";
    txt = txt.split("");
    var fsize = 14;
    var cols = c.width/fsize;
    var ds = [];
    for(var x = 0; x < cols; x++) ds[x] = 1;
    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, c.width, c.height);
        ctx.fillStyle = "#0F0";
        ctx.font = fsize + "px monospace";
        for(var i = 0; i < ds.length; i++) {
            var t = txt[Math.floor(Math.random()*txt.length)];
            ctx.fillText(t, i*fsize, ds[i]*fsize);
            if(ds[i]*fsize > c.height && Math.random() > 0.975) ds[i] = 0;
            ds[i]++;
        }
    }
    setInterval(draw, 33);
</script>
"""
components.html(matrix_vFinal, height=0)

# 3. ESTILIZAÇÃO E ORTOGRAFIA CSS
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00FF41;
            border-radius: 15px;
            padding: 20px;
        }
        .stDownloadButton button {
            width: 100% !important;
            background-color: #000 !important;
            color: #00FF41 !important;
            border: 2px solid #00FF41 !important;
            font-weight: bold !important;
        }
        [data-testid="stMetricValue"] { color: #00FF41 !important; text-align: center; font-size: 40px !important; }
        [data-testid="stMetricLabel"] { color: #00FF41 !important; text-align: center; font-size: 18px !important; }
        h3 { color: #00FF41 !important; text-align: center; text-shadow: 0 0 10px #00FF41; }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO DE DADOS (ACENTUAÇÃO CORRIGIDA)
if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. ABAS DO SISTEMA
t_rel, t_hist, t_casado, t_analise = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRICO", "📊 CASADO", "📉 ANÁLISE"])

with t_rel:
    st.write("### > TERMINAL DE OPERAÇÃO")
    item = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    val_in = st.number_input("VALOR ATUAL ($ USD):", value=banco[item]['ref'], format="%.2f")
    
    variacao = ((val_in - banco[item]['ref']) / banco[item]['ref']) * 100
    status = "ENTRA" if variacao < 10 else "PULA"
    
    if st.button("🚀 EXECUTAR REGISTRO"):
        st.session_state['logs_sentinela'].
