import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. SETUP DE COMANDO
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (FUNDO ANIMADO)
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

# 3. CSS SENTINELA (ORTOGRAFIA E ESTILO)
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

# 4. BANCO DE DADOS (CORREÇÃO DE SINTAXE E ACENTOS)
if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. ESTRUTURA OPERACIONAL
t_rel, t_hist, t_casado, t_analise = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRICO", "📊 CASADO", "📉 ANÁLISE"])

with t_rel:
    st.write("### > TERMINAL DE OPERAÇÃO")
    item = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    val_in = st.number_input("VALOR ATUAL ($ USD):", value=banco[item]['ref'], format="%.2f")
    
    var_calc = ((val_in - banco[item]['ref']) / banco[item]['ref']) * 100
    veredito = "ENTRA" if var_calc < 10 else "PULA"
    
    if st.button("🚀 REGISTRAR AUDITORIA"):
        st.session_state['logs_sentinela'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR": f"$ {val_in:.2f}",
            "VAR%": f"{var_calc:.2f}%",
            "STATUS": veredito
        })
        st.success(f"DADO REGISTRADO: {veredito}")
    
    # BOTÃO PARA GERAR RELATÓRIO FINAL (UTF-8-SIG PARA EXCEL CELULAR)
    if st.session_state['logs_sentinela']:
        df_exp = pd.DataFrame(st.session_state['logs_sentinela'])
        csv_data = df_exp.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="📥 GERAR RELATÓRIO FINAL",
            data=csv_data,
            file_name=f'Relatorio_Sentinela_{datetime.now().strftime("%H%M")}.csv',
            mime='text/csv',
        )

with t_hist:
    st.write("### > BANCO DE DADOS HISTÓRICO")
    if st.session_state['logs_sentinela']:
        st.table(pd.DataFrame(st.session_state['logs_sentinela']))

with t_casado:
    st.write("### > VISÃO CONSOLIDADA")
    df_c = pd.DataFrame([{"ITEM": k, "REF": f"$ {v['ref']:.2f}", "LIBERADO": f"{v['lib']}%", "PENDENTE": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_c)

with t_analise:
    st.write(f"### > ANÁLISE: {item}")
    c1, c2 = st.columns(2)
    with c1: st.metric("LIBERADO", f"{banco[item]['lib']}%")
    with c2: st.metric("PENDENTE", f"{banco[item]['pen']}%")
    
    fig_p = px.pie(values=[banco[item]['lib'], banco[item]['pen']], names=['LIB', 'PEN'], hole=0.7,
                   color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00FF41", showlegend=False, height=350)
    st.plotly_chart(fig_p, use_container_width=True)
