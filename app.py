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

# DESIGN MATRIX - O PADRÃO SOBERANO COM CHUVA DE CÓDIGO
st.markdown("""
    <style>
        /* Fundo Preto Absoluto e Fonte Verde Matrix */
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #000000;
            color: #00FF41;
            font-family: 'Courier Prime', monospace;
            overflow: hidden; /* Esconder scrollbar principal */
        }
        
        /* Ocultar elementos padrão */
        [data-testid="stHeader"] {visibility: hidden;
        
