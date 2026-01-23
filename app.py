import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. SETUP DE COMANDO CENTRAL
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (SANEADO)
matrix_code = """
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
components.html(matrix_code, height=0)

# 3. ESTILIZAÇÃO CSS (DESIGN NOTA FISCAL)
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.95) !important;
            border: 2px solid #00FF41;
            border-radius: 15px;
            padding: 20px;
        }
        .nota-fiscal {
            font-family: 'Courier New', Courier, monospace;
            border: 1px dashed #00FF41;
            padding: 15px;
            background-color: rgba(0, 20, 0, 0.8);
            color: #00FF41;
            margin-top: 20px;
        }
        .nota-header { border-bottom: 1px dashed #00FF41; text-align: center; margin-bottom: 10px; }
        .nota-item { display: flex; justify-content: space-between; margin-bottom: 5px; }
        .nota-footer { border-top: 1px dashed #00FF41; margin-top: 10px; padding-top: 10px; font-weight: bold; }
        .stDownloadButton button { width: 100% !important; background-color: #000 !important; color: #00FF41 !important; border: 2px solid #00FF41 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO DE DADOS
if 'logs_sentinela' not in st
