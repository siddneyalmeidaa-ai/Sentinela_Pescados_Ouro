import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. SETUP DE COMANDO
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (APENAS PARA ABAS DE TEXTO)
matrix_script = """
<canvas id="matrix_canvas"></canvas>
<style>
    body { margin: 0; overflow: hidden; background: black; }
    #matrix_canvas { position: fixed; top: 0; left: 0; z-index: -1; width: 100vw; height: 100vh; opacity: 0.5; }
</style>
<script>
    const canvas = document.getElementById('matrix_canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
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
    setInterval(rain, 33);
</script>
"""

# 3. CSS PARA ORGANIZAÇÃO E FORMATAÇÃO
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background-color: black; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00FF41;
            border-radius: 10px;
            padding: 20px;
        }
        /* Organização de Tabelas: Sem quebra de linha e Centralizado */
        .stTable td, .stTable th {
            white-space: nowrap !important;
            padding: 10px 20px !important;
            text-align: center !important;
            color: #00FF41 !important;
        }
        h1, h2, h3, p, label, .stMetric { 
            color: #00FF41 !important; 
            text-shadow: 0 0 10px #00FF41;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO DE DADOS E MEMÓRIA
if 'logs_mestre' not in st.session_state:
    st.session_state['logs_mestre'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. NAVEGAÇÃO POR ABAS
t_rel, t_hist, t_casado, t_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with t_rel:
    components.html(matrix_script, height=0) # CHUVA ATIVA AQUI
    st.write("### > ENTRADA_AUDITORIA_")
    item = st.selectbox("PRODUTO:", list(banco.keys()))
    valor = st.number_input("PREÇO ATUAL ($):", value=banco[item]['ref'], format="%.2f")
    
    variacao = ((valor - banco[item]['ref']) / banco[item]['ref']) * 100
    veredito = "ENTRA" if variacao < 10 else "PULA"
    
    if st.button("🚀 REGISTRAR"):
        st.session_state['logs_mestre'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR": f"$ {valor:.2f}",
            "VARIAÇÃO": f"{variacao:.2f}%",
            "STATUS": veredito
        })
        st.success(f"REGISTRADO: {veredito}")

with t_hist:
    components.html(matrix_script, height=0) # CHUVA ATIVA AQUI
    st.write("### > HISTÓRICO_DE_OPERAÇÕES_")
    if st.session_state['logs_mestre']:
        st.table(pd.DataFrame(st.session_state['logs_mestre']))
    else:
        st.info("SISTEMA_AGUARDANDO_DADOS")

with t_casado:
    # SEM CHUVA PARA MÁXIMA NITIDEZ DO GRÁFICO
    st.write("### > VISÃO_CONSOLIDADA_")
    df_c = pd.DataFrame([{
        "ITEM": k, "REF": f"$ {v['ref']:.2f}", "LIBERADO": f"{v['lib']}%", "PENDENTE": f"{v['pen']}%"
    } for k, v in banco.items()])
    st.table(df_c)
    
    fig_b = px.bar(df_c, x="ITEM", y=["LIBERADO", "PENDENTE"], barmode="stack", 
                   color_discrete_map={"LIBERADO": "#00FF41", "PENDENTE": "#FF0000"})
    fig_b.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color="#00FF41")
    st.plotly_chart(fig_b, use_container_width=True)

with t_analisia:
    # SEM CHUVA PARA MÁXIMA NITIDEZ DO GRÁFICO
    st.write(f"### > ANALISIA: {item}")
    st.metric("VARIAÇÃO ATUAL", f"{variacao:.2f}%")
    
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{banco[item]['lib']}%")
    c2.metric("PENDENTE", f"{banco[item]['pen']}%")
    
    fig_p = px.pie(values=[banco[item]['lib'], banco[item]['pen']], names=['LIB', 'PEN'], 
                   hole=0.6, color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_p.update_layout(paper_bgcolor='black', font_color="#00FF41", showlegend=False)
    st.plotly_chart(fig_p, use_container_width=True)
    
