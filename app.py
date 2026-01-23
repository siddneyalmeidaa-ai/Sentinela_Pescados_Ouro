import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. SETUP DE COMANDO
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (CORTINA DE FUNDO TOTAL)
matrix_v7 = """
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
components.html(matrix_v7, height=0)

# 3. CSS SENTINELA (CORREÇÃO DE DESIGN E MÉTRICAS)
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
            background-color: #000000 !important;
            color: #00FF41 !important;
            border: 2px solid #00FF41 !important;
            font-weight: bold !important;
            margin-top: 15px;
        }
        [data-testid="stMetricValue"] { font-size: 42px !important; color: #00FF41 !important; text-align: center; }
        [data-testid="stMetricLabel"] { font-size: 20px !important; color: #00FF41 !important; text-align: center; }
        h3 { color: #00FF41 !important; text-align: center; text-shadow: 0 0 10px #00FF41; }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO DE DADOS (NOMES CORRIGIDOS)
if 'logs_v3' not in st.session_state:
    st.session_state['logs_v3'] = []

# Mantendo os nomes com acentos corretos
banco = {
    'Salmão':
    
