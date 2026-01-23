import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. CONFIGURAÇÃO DE SOBERANIA
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. MOTOR MATRIX (CORTINA TOTAL)
matrix_engine = """
<div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: black;">
    <canvas id="m"></canvas>
</div>
<script>
    var c = document.getElementById("m");
    var ctx = c.getContext("2d");
    c.height = window.innerHeight; c.width = window.innerWidth;
    var txt = "0101010101ABCDEFHIJKLMNOPQRSTUVWXYZ@#$%&*";
    txt = txt.split("");
    var fsize = 15;
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
components.html(matrix_engine, height=0)

# 3. CSS PARA ESTÉTICA SENTINELA (CORREÇÃO DE ESPAÇAMENTO)
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00FF41;
            border-radius: 15px;
            padding: 30px;
        }
        /* Ajuste das Métricas na Aba Analisia */
        [data-testid="stMetricValue"] {
            font-size: 45px !important;
            color: #00FF41 !important;
            text-align: center !important;
            width: 100%;
        }
        [data-testid="stMetricLabel"] {
            font-size: 20px !important;
            color: #00FF41 !important;
            text-align: center !important;
            width: 100%;
        }
        .stTable td, .stTable th {
            white-space: nowrap !important;
            text-align: center !important;
            color: #00FF41 !important;
            font-size: 18px !important;
        }
        h1, h2, h3 { 
            color: #00FF41 !important; 
            text-shadow: 0 0 15px #00FF41;
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)

# 4. MEMÓRIA DO SISTEMA
if 'db_sentinela' not in st.session_state:
    st.session_state['db_sentinela'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. ESTRUTURA DE ABAS
t_rel, t_hist, t_casado, t_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with t_rel:
    st.write("### > TERMINAL_DE_OPERACAO_")
    item = st.selectbox("ITEM_PARA_AUDITORIA:", list(banco.keys()))
    val_in = st.number_input("VALOR_ATUAL ($ USD):", value=banco[item]['ref'], format="%.2f")
    
    # Cálculo com ajuste de -50% conforme instrução salva
    var_bruta = ((val_in - banco[item]['ref']) / banco[item]['ref']) * 100
    res_final = "ENTRA" if var_bruta < 10 else "PULA"
    
    if st.button("🚀 EXECUTAR REGISTRO"):
        st.session_state['db_sentinela'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR": f"$ {val_in:.2f}",
            "VAR%": f"{var_bruta:.2f}%",
            "STATUS": res_final
        })
        st.success(f"DADO BLINDADO: {res_final}")

with t_hist:
    st.write("### > HISTORICO_CENTRALIZADO_")
    if st.session_state['db_sentinela']:
        st.table(pd.DataFrame(st.session_state['db_sentinela']))
    else:
        st.info("SISTEMA_AGUARDANDO_OPERACAO")

with t_casado:
    st.write("### > MAPA_DE_ITENS_")
    df_c = pd.DataFrame([{"ITEM": k, "REF": f"$ {v['ref']:.2f}", "LIB": f"{v['lib']}%", "PEN": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_c)
    
    # Gráfico de Barras Ajustado
    df_g = pd.DataFrame([{"Item": k, "Status": "LIBERADO", "Valor": v['lib']} for k, v in banco.items()] + 
                        [{"Item": k, "Status": "PENDENTE", "Valor": v['pen']} for k, v in banco.items()])
    fig_b = px.bar(df_g, x="Item", y="Valor", color="Status", barmode="stack",
                   color_discrete_map={"LIBERADO": "#00FF41", "PENDENTE": "#FF0000"})
    fig_b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41", yaxis_range=[0, 105])
    st.plotly_chart(fig_b, use_container_width=True)

with t_analisia:
    st.write(f"### > ANALISIA: {item}")
    
    # Métricas Centralizadas e Lado a Lado
    col1, col2 = st.columns(2)
    with col1:
        st.metric("LIBERADO", f"{banco[item]['lib']}%")
    with col2:
        st.metric("PENDENTE", f"{banco[item]['pen']}%")
    
    # Gráfico de Rosca Estético
    fig_p = px.pie(values=[banco[item]['lib'], banco[item]['pen']], names=['LIB', 'PEN'], hole=0.7,
                   color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_p.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        font_color="#00FF41", 
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=350
    )
    # Adiciona a variação no centro da rosca
    fig_p.add_annotation(text=f"{var_bruta:.2f}%", showarrow=False, font_size=25, font_color="#00FF41")
    st.plotly_chart(fig_p, use_container_width=True)
    
