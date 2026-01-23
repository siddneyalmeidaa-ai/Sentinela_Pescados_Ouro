import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. CONFIGURAÇÃO DE COMANDO CENTRAL
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (CÓDIGO BLINDADO)
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
        ctx
        
