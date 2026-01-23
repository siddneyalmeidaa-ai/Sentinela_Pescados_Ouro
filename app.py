import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. SETUP DE COMANDO
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (CORTINA DE FUNDO)
matrix_v6 = """
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
components.html(matrix_v6, height=0)

# 3. CSS SENTINELA (AJUSTE DE BOTÕES E MÉTRICAS)
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00FF41;
            border-radius: 15px;
            padding: 20px;
        }
        /* Botão Gerar Relatório - Estilo Especial */
        .stDownloadButton button {
            width: 100% !important;
            background-color: #000000 !important;
            color: #00FF41 !important;
            border: 2px solid #00FF41 !important;
            font-weight: bold !important;
            text-shadow: 0 0 10px #00FF41;
        }
        [data-testid="stMetricValue"] { font-size: 40px !important; color: #00FF41 !important; text-align: center; }
        [data-testid="stMetricLabel"] { font-size: 18px !important; color: #00FF41 !important; text-align: center; }
        h3 { color: #00FF41 !important; text-align: center; text-shadow: 0 0 10px #00FF41; }
    </style>
""", unsafe_allow_html=True)

# 4. MEMÓRIA
if 'logs' not in st.session_state:
    st.session_state['logs'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. INTERFACE
t_rel, t_hist, t_casado, t_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with t_rel:
    st.write("### > TERMINAL_DE_OPERACAO_")
    item = st.selectbox("ITEM_PARA_AUDITORIA:", list(banco.keys()))
    val_at = st.number_input("VALOR_ATUAL ($ USD):", value=banco[item]['ref'], format="%.2f")
    
    var = ((val_at - banco[item]['ref']) / banco[item]['ref']) * 100
    res = "ENTRA" if var < 10 else "PULA"
    
    if st.button("🚀 EXECUTAR REGISTRO"):
        st.session_state['logs'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR": f"$ {val_at:.2f}",
            "VAR%": f"{var:.2f}%",
            "STATUS": res
        })
        st.success(f"DADO BLINDADO: {res}")
    
    st.markdown("---")
    # BOTÃO SOLICITADO: GERAR RELATÓRIO (DOWNLOAD CSV)
    if st.session_state['logs']:
        df_download = pd.DataFrame(st.session_state['logs'])
        csv = df_download.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 GERAR RELATÓRIO FINAL",
            data=csv,
            file_name=f'relatorio_sentinela_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )
    else:
        st.warning("AGUARDANDO DADOS PARA GERAR RELATÓRIO")

with t_hist:
    st.write("### > BANCO_DE_DADOS_HISTORICO_")
    if st.session_state['logs']:
        st.table(pd.DataFrame(st.session_state['logs']))

with t_casado:
    st.write("### > VISÃO_CONSOLIDADA_")
    df_c = pd.DataFrame([{"ITEM": k, "REF": f"$ {v['ref']:.2f}", "LIB": f"{v['lib']}%", "PEN": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_c)
    
    df_g = pd.DataFrame([{"Item": k, "Status": "LIBERADO", "Valor": v['lib']} for k, v in banco.items()] + 
                        [{"Item": k, "Status": "PENDENTE", "Valor": v['pen']} for k, v in banco.items()])
    fig_b = px.bar(df_g, x="Item", y="Valor", color="Status", barmode="stack",
                   color_discrete_map={"LIBERADO": "#00FF41", "PENDENTE": "#FF0000"})
    fig_b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41", yaxis_range=[0, 105])
    st.plotly_chart(fig_b, use_container_width=True)

with t_analisia:
    st.write(f"### > ANALISIA: {item}")
    c1, c2 = st.columns(2)
    
