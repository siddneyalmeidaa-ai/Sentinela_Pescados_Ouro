import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP DE SOBERANIA
st.set_page_config(page_title="SPA IA SENTINELA", layout="wide")

# 2. DESIGN MATRIX COM CHUVA E RELATÓRIO VISÍVEL
st.markdown("""
    <style>
        /* CHUVA DE CÓDIGOS MATRIX EM CSS PURO (NÃO FALHA) */
        [data-testid="stAppViewContainer"] {
            background: black;
            background-image: linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            position: relative;
            overflow: hidden;
        }
        
        [data-testid="stAppViewContainer"]::before {
            content: "101011010010101011010101010101010110101010101011010101010";
            position: absolute;
            top: -100px;
            left: 0;
            width: 100%;
            color: #00FF41;
            font-family: monospace;
            font-size: 20px;
            white-space: nowrap;
            animation: matrix_rain 5s linear infinite;
            opacity: 0.3;
            z-index: 0;
        }

        @keyframes matrix_rain {
            0% { transform: translateY(0); }
            100% { transform: translateY(100vh); }
        }

        /* ESTILO DAS ABAS E TEXTOS */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(0, 0, 0, 0.85) !important;
            border: 2px solid #00FF41;
            padding: 20px;
            border-radius: 10px;
            z-index: 1;
        }

        h1, h2, h3, p, label, .stMetric { 
            color: #00FF41 !important; 
            text-shadow: 0 0 8px #00FF41; 
        }
        
        button[data-baseweb="tab"] { color: #00FF41 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. BANCO DE DADOS E MEMÓRIA DO RELATÓRIO
if 'banco_logs' not in st.session_state:
    st.session_state['banco_logs'] = []

banco_fixo = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 4. SISTEMA DE ABAS
t_rel, t_hist, t_casado, t_analisia = st.tabs(["📑 RELATÓRIO", "📜 HISTÓRIO", "📊 CASADO", "📉 ANALISIA"])

with t_rel:
    st.write("### > INPUT_SISTEMA_SENTINELA")
    item = st.selectbox("IDENTIFIQUE O ITEM:", list(banco_fixo.keys()))
    val_input = st.number_input("VALOR ATUAL (USD):", value=banco_fixo[item]['ref'])
    
    # Cálculo de Auditoria
    ref = banco_fixo[item]['ref']
    variacao = ((val_input - ref) / ref) * 100
    veredito = "ENTRA" if variacao < 10 else "PULA"
    cor_v = "🟢" if veredito == "ENTRA" else "🔴"

    if st.button("🚀 REGISTRAR AUDITORIA"):
        # GERA O RELATÓRIO NA HORA E SALVA NA MEMÓRIA
        novo_registro = {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "PREÇO": f"${val_input:.2f}",
            "X%": f"{variacao:.2f}%",
            "VEREDITO": veredito
        }
        st.session_state['banco_logs'].insert(0, novo_registro)
        st.success(f"SISTEMA ATUALIZADO: {cor_v} {veredito}")

with t_hist:
    st.write("### > RELATÓRIO_DE_AUDITORIA_GERADO")
    if st.session_state['banco_logs']:
        # Exibe o relatório em formato de tabela profissional
        df_logs = pd.DataFrame(st.session_state['banco_logs'])
        st.table(df_logs)
        
        # Botão para baixar o relatório (Auditoria)
        csv = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button("📥 BAIXAR RELATÓRIO CSV", csv, "auditoria_spa.csv", "text/csv")
    else:
        st.warning("AGUARDANDO REGISTROS PARA GERAR RELATÓRIO...")

with t_casado:
    st.write("### > MAPA_DE_ITENS_CONSOLIDADO")
    df_c = pd.DataFrame([{"ITEM": k, "REF": v['ref'], "LIBERADO": v['lib'], "PENDENTE": v['pen']} for k, v in banco_fixo.items()])
    st.table(df_c)
    
    fig_barra = px.bar(df_c, x="ITEM", y=["LIBERADO", "PENDENTE"], barmode="stack", 
                       color_discrete_map={"LIBERADO": "#00FF41", "PENDENTE": "#FF0000"})
    fig_barra.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_barra, use_container_width=True)

with t_analisia:
    st.write(f"### > ANÁLISE_SENSORIAL: {item}")
    c1, c2 = st.columns(2)
    c1.metric("STATUS_LIBERADO", f"{banco_fixo[item]['lib']}%")
    c2.metric("STATUS_PENDENTE", f"{banco_fixo[item]['pen']}%")
    
    fig_pizza = px.pie(values=[banco_fixo[item]['lib'], banco_fixo[item]['pen']], names=['LIB', 'PEN'], 
                 hole=0.6, color_discrete_sequence=['#00FF41', '#FF0000'])
    fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig_pizza, use_container_width=True)
    
