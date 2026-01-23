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
        [data-testid="stHeader"] {visibility: hidden; height: 0px;}
        footer {display:none !important;}
        .stActionButton {display: none;} /* Oculta o botão de menu */
        [data-testid="stStatusWidget"] {display: none;}
        div[data-testid="stDecoration"] {display:none;}
        
        /* Ajuste do container principal para acomodar a chuva de código */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            position: relative;
            z-index: 1; /* Garante que o conteúdo fique acima do canvas */
        }

        /* Estilização de Métricas */
        [data-testid="stMetricValue"] {
            color: #00FF41 !important;
            text-shadow: 0 0 10px #00FF41;
            font-size: 2.5rem !important;
        }
        [data-testid="stMetricLabel"] {
            color: #00FF41 !important;
            letter-spacing: 2px;
        }

        /* Botão S.P.A. Estilo Terminal */
        .stButton>button {
            background-color: #000000;
            color: #00FF41;
            border: 2px solid #00FF41;
            border-radius: 0px;
            width: 100%;
            height: 3em;
            font-weight: bold;
            text-transform: uppercase;
            box-shadow: 0 0 15px #00FF41;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #00FF41;
            color: #000000;
        }

        /* Tabs Matrix */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #000000;
        }
        .stTabs [data-baseweb="tab"] {
            color: #00FF41 !important;
            text-shadow: 0 0 5px #00FF41;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #00FF41 !important;
            background-color: rgba(0, 255, 65, 0.1);
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #00FF41 !important;
            background-color: rgba(0, 255, 65, 0.2);
            border-bottom: 2px solid #00FF41;
        }

        /* Tabelas Matrix */
        .stDataFrame, div[data-testid="stTable"] {
            border: 1px solid #00FF41;
            color: #00FF41;
            background-color: rgba(0,0,0,0.5); /* Semi-transparente para ver o fundo */
        }
        
        /* Campos de Input */
        .st-bq, .st-ck, .st-cl { /* Seleciona os campos de input e selectbox */
            background-color: rgba(0, 255, 65, 0.1);
            border: 1px solid #00FF41;
            color: #00FF41;
            padding: 0.5rem;
            border-radius: 5px;
        }
        .st-bq>div>div>div>input, .st-ck>div>div>div>input, .st-cl>div>div>div>input {
            color: #00FF41 !important;
        }
        
        /* Cor dos títulos e captions */
        h1, h2, h3, h4, h5, h6 {
            color: #00FF41 !important;
            text-shadow: 0 0 8px #00FF41;
        }
        .st-bc { /* Caption */
            color: #00FF41 !important;
            opacity: 0.8;
        }

        /* Chuva de Código - Canvas e JS */
        #matrixCanvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0; /* Fica no fundo */
        }
    </style>
    
    <canvas id="matrixCanvas"></canvas>
    
    <script>
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズヅブプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
        const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const nums = '0123456789';
        const chars = katakana + latin + nums;

        const fontSize = 16;
        const columns = canvas.width / fontSize;

        const drops = [];
        for (let i = 0; i < columns; i++) {
            drops[i] = 1;
        }

        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00FF41'; // Cor verde Matrix
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }

        setInterval(draw, 33); // Velocidade da chuva de código

        // Resizer para manter a chuva de código responsiva
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const newColumns = canvas.width / fontSize;
            while(drops.length < newColumns) drops.push(1);
            while(drops.length > newColumns) drops.pop();
        });

    </script>
""", unsafe_allow_html=True)


# 2. BANCO DE DADOS - PADRÃO OURO
banco = {
    'Salmao':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarao':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilapia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. INTERFACE OPERACIONAL
aba_ajuste, aba_dash, aba_casado, aba_hist = st.tabs([
    "📟 TERMINAL", "📈 MATRIX_DASH", "📊 CONSOLIDADO", "📂 REGISTROS"
])

with aba_ajuste:
    st.markdown("### > SPA_IA_SENTINELA_v2.0_")
    item_sel = st.selectbox("IDENTIFIQUE O ITEM:", list(banco.keys()))
    preco_atual = st.number_input(f"VALOR_INPUT (USD):", value=banco[item_sel]['ref'], step=0.10, format="%.2f")
    
    dados = banco[item_sel]
    x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
    
    # Adicionando o "VÁCUO" conforme o manual
    if preco_atual == 1.0: # Regra de negócio para preço inválido
        veredito = "VÁCUO"; cor = "🔴"
    elif x_calc >= 10: 
        veredito = "PULA"; cor = "🟡"
    else: 
        veredito = "ENTRA"; cor = "🟢"

    if st.button("EXEC_AUDITORIA"):
        st.session_state.setdefault('historico_dia', []).insert(0, {
            "Hora": datetime.now().strftime("%H:%M"),
            "Item": item_sel,
            "Variação": f"{x_calc:.2f}%",
            "Veredito": veredito
        })
        st.toast(f"LOG_REGISTRADO: {veredito}")

with aba_dash:
    st.caption(f"STATUS_REPORT: {item_sel}")
    
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{dados['lib']}%")
    c2.metric("PENDENTE", f"{dados['pen']}%")
    
    st.markdown(f"### VEREDITO: {cor} {veredito}")
    
    # Gráfico Matrix Colors
    fig_ind = px.pie(
        values=[dados['lib'], dados['pen']], 
        names=['LIBERADO', 'PENDENTE'], 
        hole=0.6,
        color_discrete_sequence=['#00FF41', '#FF0000']
    )
    fig_ind.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#00FF41",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_ind, use_container_width=True, config={'displayModeBar': False})

with aba_casado:
    st.caption("VISÃO_ESTRUTURAL_PEIXES")
    df_v = pd.DataFrame([{"ITEM": k, "REF": f"${v['ref']:.2f}", "LIB": f"{v['lib']}%", "PEN": f"{v['pen']}%"} for k, v in banco.items()])
    st.table(df_v)

with aba_hist:
    st.caption("LOG_SISTEMA_AUDITORIA")
    if 'historico_dia' in st.session_state and st.session_state['historico_dia']:
        df_r = pd.DataFrame(st.session_state['historico_dia'])
        st.table(df_r)
        csv = df_r.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 BAIXAR_LOG_S.P.A.", csv, "auditoria_spa.csv", "text/csv")

