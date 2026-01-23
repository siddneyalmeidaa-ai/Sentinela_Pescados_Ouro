import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR DA CHUVA MATRIX (JAVASCRIPT CANVAS - O ÚNICO QUE FUNCIONA REAL)
matrix_engine = """
<canvas id="canvas"></canvas>
<style>
    body { margin: 0; overflow: hidden; background: black; }
    canvas { position: fixed; top: 0; left: 0; z-index: -1; width: 100vw; height: 100vh; }
</style>
<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*";
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);
    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#0F0";
        ctx.font = fontSize + "px monospace";
        for (let i = 0; i < drops.length; i++) {
            const text = letters.charAt(Math.floor(Math.random() * letters.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 33);
</script>
"""
components.html(matrix_engine, height=0) # Injeta a chuva no background

# 3. CSS PARA IDENTIDADE VISUAL E ABAS
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.85) !important;
            border: 2px solid #00FF41;
            border-radius: 10px;
            padding: 20px;
        }
        h1, h2, h3, p, label, .stMetric { 
            color: #00FF41 !important; 
            text-shadow: 0 0 10px #00FF41; 
            font-family: 'Courier New', monospace;
        }
        button[data-baseweb="tab"] { color: #00FF41 !important; font-size: 18px !important; }
    </style>
""", unsafe_allow_html=True)

# 4. MEMÓRIA DO RELATÓRIO (SESSION STATE)
if 'relatorio_final' not in st.session_state:
    st.session_state['relatorio_final'] = []

banco_ouro = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. ABAS OPERACIONAIS
aba_rel, aba_hist, aba_casado, aba_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with aba_rel:
    st.write("### > ACESSANDO_TERMINAL_SENTINELA_")
    item = st.selectbox("IDENTIFIQUE O ITEM:", list(banco_ouro.keys()))
    preco = st.number_input("VALOR_ATUAL (USD):", value=banco_ouro[item]['ref'])
    
    variacao = ((preco - banco_ouro[item]['ref']) / banco_ouro[item]['ref']) * 100
    veredito = "ENTRA" if variacao < 10 else "PULA"
    cor_v = "🟢" if veredito == "ENTRA" else "🔴"

    if st.button("🚀 REGISTRAR AUDITORIA"):
        # GRAVAÇÃO REAL NO RELATÓRIO
        log = {
            "DATA_HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR": f"${preco:.2f}",
            "VARIAÇÃO": f"{variacao:.2f}%",
            "STATUS": veredito
        }
        st.session_state['relatorio_final'].insert(0, log)
        st.success(f"REGISTRO EFETUADO: {cor_v} {veredito}")

with aba_hist:
    st.write("### > BANCO_DE_DADOS_HISTÓRICO")
    if st.session_state['relatorio_final']:
        df_hist = pd.DataFrame(st.session_state['relatorio_final'])
        st.table(df_hist) # Exibe o relatório gerado
    else:
        st.info("SISTEMA_AGUARDANDO_DADOS_PARA_GERAR_RELATÓRIO")

with aba_casado:
    st.write("### > VISÃO_CONSOLIDADA_S.A.")
    df_c = pd.DataFrame([{"ITEM": k, "REF": v['ref'], "LIB": v['lib'], "PEN": v['pen']} for k, v in banco_ouro.items()])
    st.table(df_c)
    fig_b = px.bar(df_c, x="ITEM", y=["LIB", "PEN"], barmode="stack", color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_b, use_container_width=True)

with aba_analisia:
    st.metric(f"ANALISIA: {item}", f"{variacao:.2f}%")
    fig_p = px.pie(values=[banco_ouro[item]['lib'], banco_ouro[item]['pen']], names=['LIB', 'PEN'], hole=0.6, color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_p, use_container_width=True)
    
