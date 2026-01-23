import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. SETUP DE SOBERANIA
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX V3 (CHUVA DENSA E FLUIDA)
matrix_v3 = """
<canvas id="matrix_canvas"></canvas>
<style>
    body { margin: 0; overflow: hidden; background: black; }
    #matrix_canvas {
        position: fixed; top: 0; left: 0; z-index: -1;
        width: 100vw; height: 100vh;
    }
</style>
<script>
    const canvas = document.getElementById('matrix_canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$#@%";
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);
    function rain() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#0F0";
        ctx.font = fontSize + "px monospace";
        for (let i = 0; i < drops.length; i++) {
            const text = chars.charAt(Math.floor(Math.random() * chars.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(rain, 30);
</script>
"""
components.html(matrix_v3, height=0)

# 3. CSS PARA ORGANIZAÇÃO DE TABELAS E CENTRALIZAÇÃO
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00FF41;
            border-radius: 10px;
            padding: 20px;
        }
        /* Ajuste para tabela não quebrar texto */
        .stTable td, .stTable th {
            white-space: nowrap !important;
            text-align: center !important;
            color: #00FF41 !important;
        }
        h1, h2, h3, p, label, .stMetric { 
            color: #00FF41 !important; 
            text-shadow: 0 0 10px #00FF41;
            text-align: center;
        }
        div[data-testid="stMetricValue"] { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO E HISTÓRICO
if 'historico_mestre' not in st.session_state:
    st.session_state['historico_mestre'] = []

banco_peixes = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. NAVEGAÇÃO
t_rel, t_hist, t_casado, t_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with t_rel:
    st.write("### > ENTRADA_DADOS_TERMINAL_")
    item = st.selectbox("PRODUTO:", list(banco_peixes.keys()))
    valor = st.number_input("PREÇO ($):", value=banco_peixes[item]['ref'], format="%.2f")
    
    calc_x = ((valor - banco_peixes[item]['ref']) / banco_peixes[item]['ref']) * 100
    res = "ENTRA" if calc_x < 10 else "PULA"
    
    if st.button("🚀 REGISTRAR AUDITORIA"):
        st.session_state['historico_mestre'].insert(0, {
            "DATA_HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR": f"$ {valor:.2f}",
            "VARIAÇÃO": f"{calc_x:.2f}%",
            "STATUS": res
        })
        st.success(f"DADO GRAVADO: {res}")

with t_hist:
    st.write("### > BANCO_DE_DADOS_HISTORICO_")
    if st.session_state['historico_mestre']:
        st.table(pd.DataFrame(st.session_state['historico_mestre']))
    else:
        st.info("SISTEMA_VAZIO")

with t_casado:
    st.write("### > VISÃO_CONSOLIDADA_S.A_")
    df_view = pd.DataFrame([{
        "ITEM": k, 
        "REF": f"$ {v['ref']:.2f}", 
        "LIBERADO": f"{v['lib']}%", 
        "PENDENTE": f"{v['pen']}%"
    } for k, v in banco_peixes.items()])
    st.table(df_view)
    
    fig_b = px.bar(df_view, x="ITEM", y=[85, 60, 95], # Exemplificando valores fixos para o gráfico
                   color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_b, use_container_width=True)

with t_analisia:
    st.write(f"### > ANALISIA: {item}")
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{banco_peixes[item]['lib']}%")
    c2.metric("PENDENTE", f"{banco_peixes[item]['pen']}%")
    
    fig_pie = px.pie(values=[banco_peixes[item]['lib'], banco_peixes[item]['pen']], 
                     names=['LIB', 'PEN'], hole=0.6, color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_pie, use_container_width=True)
    
