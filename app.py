import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# 1. CONFIGURAÇÃO DE COMANDO
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

# 3. ESTILIZAÇÃO CSS (INTERFACE NOTA FISCAL MOBILE)
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: transparent !important; }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.95) !important;
            border: 2px solid #00FF41;
            border-radius: 15px;
            padding: 15px;
        }
        .nota-fiscal {
            font-family: 'Courier New', Courier, monospace;
            border: 1px dashed #00FF41;
            padding: 15px;
            background-color: rgba(0, 20, 0, 0.9);
            color: #00FF41;
            margin-top: 15px;
        }
        .nota-header { border-bottom: 1px dashed #00FF41; text-align: center; padding-bottom: 10px; margin-bottom: 10px; }
        .nota-item { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.85em; }
        .nota-total { border-top: 2px solid #00FF41; margin-top: 10px; padding-top: 10px; font-weight: bold; font-size: 1.1em; }
        .stDownloadButton button { width: 100% !important; background-color: #000 !important; color: #00FF41 !important; border: 2px solid #00FF41 !important; }
        h3 { color: #00FF41 !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 4. BANCO DE DADOS
if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 5. ABAS DESMEMBRADAS (FOCO EM OPERAÇÃO)
t_term, t_rel, t_casado, t_analise = st.tabs(["🎮 TERMINAL", "📑 RELATÓRIO", "📊 CASADO", "📉 ANÁLISE"])

# --- ABA 1: TERMINAL (AÇÃO RÁPIDA) ---
with t_term:
    st.write("### > ENTRADA DE DADOS")
    item_op = st.selectbox("PRODUTO:", list(banco.keys()))
    val_op = st.number_input("VALOR ATUAL ($):", value=banco[item_op]['ref'], format="%.2f")
    
    variacao = ((val_op - banco[item_op]['ref']) / banco[item_op]['ref']) * 100
    status_op = "ENTRA" if variacao < 10 else "PULA"
    
    if st.button("🚀 EFETUAR REGISTRO"):
        st.session_state['logs_sentinela'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item_op,
            "VALOR": val_op, # Número puro para cálculo seguro
            "VAR%": f"{variacao:.2f}%",
            "STATUS": status_op
        })
        st.success(f"DADO REGISTRADO: {item_op}")

# --- ABA 2: RELATÓRIO (RESUMO NOTA FISCAL) ---
with t_rel:
    st.write("### > AUDITORIA DE EXPEDIENTE")
    if st.session_state['logs_sentinela']:
        df = pd.DataFrame(st.session_state['logs_sentinela'])
        
        # Tabela visual para conferência rápida
        st.table(df)
        
        # --- DESIGN NOTA FISCAL (CÁLCULO BLINDADO) ---
        total_acumulado = sum(d['VALOR'] for d in st.session_state['logs_sentinela'])
        
        st.markdown(f"""
        <div class="nota-fiscal">
            <div class="nota-header">
                <b>*** CUPOM DE AUDITORIA ***</b><br>
                SENTINELA IA - GESTÃO DE ATIVOS<br>
                DATA: {datetime.now().strftime('%d/%m/%Y')} | HORA: {datetime.now().strftime('%H:%M')}
            </div>
        """, unsafe_allow_html=True)
        
        for idx, row in df.iterrows():
            st.markdown(f"""
            <div class="nota-item">
                <span>{row['ITEM']} [{row['HORA']}]</span>
                <span>$ {row['VALOR']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
            <div class="nota-total">
                <div class="nota-item">
                    <span>REGISTROS TOTAIS:</span>
                    <span>{len(df)}</span>
                </div>
                <div class="nota-item">
                    <span>VALOR TOTAL ACUMULADO:</span>
                    <span>$ {total_acumulado:.2f}</span>
                </div>
            </div>
            <div style="text-align: center; margin-top: 15px; font-size: 0.7em;">
                ID DA SESSÃO: {hex(id(st.session_state))}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Exportação Mobile Corrigida (Evita corrupção de acentos)
        csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 BAIXAR EXCEL SANEADO", data=csv, 
                           file_name=f"Relatorio_{datetime.now().strftime('%H%M')}.csv", mime="text/csv")
    else:
        st.info("SISTEMA AGUARDANDO COMANDOS NO TERMINAL.")

# --- ABA 3: CASADO ---
with t_casado:
    st.write("### > VISÃO CONSOLIDADA")
    df_c = pd.DataFrame([{"ITEM": k, "REF": f"$ {v['ref']:.2f}", "LIBERADO": f"{v['lib']}%"} for k, v in banco.items()])
    st.table(df_c)

# --- ABA 4: ANÁLISE ---
with t_analise:
    st.write(f"### > DESEMPENHO: {item_op}")
    st.metric("LIBERADO", f"{banco[item_op]['lib']}%")
    fig = px.pie(values=[banco[item_op]['lib'], banco[item_op]['pen']], names=['LIB', 'PEN'], hole=0.7,
                 color_discrete_sequence=['#00FF41', '#FF0000'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00FF41", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
        
