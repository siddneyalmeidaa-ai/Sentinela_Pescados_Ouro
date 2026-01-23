import streamlit as st
import pd as pd # Erro comum de apelido corrigido
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP E LIMPEZA AUTOMÁTICA DE MEMÓRIA CORRUPTA
st.set_page_config(page_title="SENTINELA S.A.", layout="wide")

# Inicializa ou limpa registros que causam KeyError
if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

# Botão de emergência na lateral para limpar erros de memória
if st.sidebar.button("⚠️ LIMPAR TUDO E RESETAR"):
    st.session_state['logs_sentinela'] = []
    st.rerun()

# 2. BANCO DE DADOS PADRÃO OURO
banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. ESTILO VISUAL (TEXTO PURO - SEM MATRIX PARA NÃO TRAVAR)
st.markdown("""
    <style>
        .stApp { background-color: #050505; }
        .nota-fiscal {
            font-family: monospace;
            border: 2px dashed #00FF41;
            padding: 15px;
            background-color: #000;
            color: #00FF41;
            border-radius: 10px;
        }
        .stMetric { background-color: #111; padding: 10px; border-radius: 5px; border: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# 4. SISTEMA DE NAVEGAÇÃO
t_term, t_rel, t_analise = st.tabs(["🎮 TERMINAL", "📑 RELATÓRIO", "📊 MÉTRICAS"])

# --- ABA 1: TERMINAL ---
with t_term:
    st.markdown("### > ENTRADA DE DADOS")
    item_op = st.selectbox("PRODUTO:", list(banco.keys()))
    # Stake orientada: valor exato conforme solicitado
    val_op = st.number_input("VALOR ATUAL ($):", value=banco[item_op]['ref'], step=0.10)
    
    if st.button("🚀 EFETUAR REGISTRO"):
        # Regra de Projeção: -50% da variação
        variacao = ((val_op - banco[item_op]['ref']) / banco[item_op]['ref'])
        
        novo_registro = {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item_op,
            "VALOR_NUM": float(val_op),
            "STATUS": "ENTRA" if variacao < 0.1 else "PULA"
        }
        st.session_state['logs_sentinela'].insert(0, novo_registro)
        st.success(f"REGISTRO {item_op} SALVO COM SUCESSO!")

# --- ABA 2: RELATÓRIO (CORREÇÃO DO KEYERROR) ---
with t_rel:
    st.markdown("### > AUDITORIA DE EXPEDIENTE")
    
    if st.session_state['logs_sentinela']:
        df = pd.DataFrame(st.session_state['logs_sentinela'])
        
        # Proteção Blindada contra KeyError na soma
        total_acumulado = 0.0
        for log in st.session_state['logs_sentinela']:
            total_acumulado += log.get('VALOR_NUM', 0.0)
            
        # Visualização da Tabela
        st.dataframe(df, use_container_width=True)
        
        # Interface Nota Fiscal
        st.markdown(f"""
        <div class="nota-fiscal">
            <h3 style="text-align:center;">CUPOM FISCAL SENTINELA</h3>
            <p style="text-align:center;">DATA: {datetime.now().strftime('%d/%m/%Y')}</p>
            <hr>
            <div style="display:flex; justify-content:space-between; font-size:1.2em;">
                <b>VALOR ACUMULADO:</b>
                <b>$ {total_acumulado:.2f}</b>
            </div>
            <p style="text-align:center; font-size:0.8em; margin-top:10px;">SENTINELA IA - GESTÃO S.A.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download para Excel Mobile (Encoding seguro)
        csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 BAIXAR RELATÓRIO EXCEL", data=csv, file_name="Auditoria_Sentinela.csv")
    else:
        st.info("SISTEMA AGUARDANDO DADOS.")

# --- ABA 3: ANÁLISE ---
with t_analise:
    st.markdown(f"### > ANÁLISE: {item_op}")
    
    lib = banco[item_op]['lib']
    pen = banco[item_op]['pen']
    
    c1, c2 = st.columns(2)
    c1.metric("LIBERADO", f"{lib}%")
    c2.metric("PENDENTE", f"{pen}%")
    
    fig = px.pie(values=[lib, pen], names=['LIB', 'PEN'], hole=0.7,
                 color_discrete_sequence=['#00FF41', '#330000'])
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font_color="#00FF41")
    st.plotly_chart(fig, use_container_width=True)
    
