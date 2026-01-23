import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. CONFIGURAÇÃO DE SOBERANIA
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (CHUVA TOTAL NO FUNDO)
matrix_final = """
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
components.html(matrix_final, height=0)

# 3. CSS DE ALINHAMENTO E TRANSPARÊNCIA
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00FF41;
            border-radius: 10px;
            padding: 15px;
        }
        .stTable td, .stTable th {
            white-space: nowrap !important;
            text-align: center !important;
            color: #00FF41 !important;
            padding: 10px !important;
        }
        h1, h2, h3, p, label, .stMetric { 
            color: #00FF41 !important; 
            text-shadow: 0 0 10px #00FF41;
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO DE DADOS
if 'relatorio_logs' not in st.session_state:
    st.session_state['relatorio_logs'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. ABAS
t_rel, t_hist, t_casado, t_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with t_rel:
    st.write("### > INPUT_SISTEMA_")
    item = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    val = st.number_input("VALOR ATUAL ($):", value=banco[item]['ref'], format="%.2f")
    var = ((val - banco[item]['ref']) / banco[item]['ref']) * 100
    res = "ENTRA" if var < 10 else "PULA"
    
    if st.button("🚀 EXECUTAR_AUDITORIA"):
        st.session_state['relatorio_logs'].insert(0, {
            "DATA_HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "PREÇO": f"$ {val:.2f}",
            "VAR%": f"{var:.2f}%",
            "STATUS": res
        })
        st.success(f"DADO REGISTRADO: {res}")

with t_hist:
    st.write("### > BANCO_DE_DADOS_")
    if st.session_state['relatorio_logs']:
        st.table(pd.DataFrame(st.session_state['relatorio_logs']))
    else:
        st.info("SEM REGISTROS NO MOMENTO")

with t_casado:
    st.write("### > CONSOLIDADO_S.A_")
    # Tabela com nomes corrigidos
    df_t = pd.DataFrame([{"ITEM": k, "REF": f"$ {v['ref']:.2f}", "LIBERADO": f"{v['lib']}%", "PENDENTE": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_t)
    
    # Gráfico de Barras Consertado (Sem erro de sintaxe)
    df_g = pd.DataFrame([{"Item": k, "Status": "LIBERADO", "Valor": v['lib']} for k, v in banco.items()] + 
                        [{"Item": k, "Status": "PENDENTE", "Valor": v['pen']} for k, v in banco.items()])
    
    fig_b = px.bar(df_g, x="Item", y="Valor", color="Status", barmode="stack",
                   color_discrete_map={"LIBERADO": "#00FF41", "PENDENTE": "#FF0000"})
    fig_b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41", 
                       yaxis_range=[0, 100])
    st.plotly_chart(fig_b, use_container_width=True)

with t_analisia:
    st.write(f"### > ANALISIA: {item}")
    c1, c2 = st.columns(2)
    c1.metric("LIB", f"{banco[item]['lib']}%")
    c2.metric("PEN", f"{banco[item]['pen']}%")
    
    fig_p = px.pie(values=[banco[item]['lib'], banco[item]['pen']], names=['LIB', 'PEN'], hole=0.6,
                   color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00FF41", showlegend=False)
    st.plotly_chart(fig_p, use_container_width=True)
    
