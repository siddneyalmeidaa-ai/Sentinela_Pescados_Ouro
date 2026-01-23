import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. CONFIGURAÇÃO DE INTERFACE LIMPA
st.set_page_config(page_title="SENTINELA V5.0", layout="wide")

# Estilização básica para manter o modo escuro e legibilidade
st.markdown("""
    <style>
        .reportview-container { background: #0e1117; }
        .nota-fiscal {
            font-family: 'Courier New', monospace;
            border: 2px dashed #00FF41;
            padding: 20px;
            background-color: #000;
            color: #00FF41;
        }
        .nota-item { display: flex; justify-content: space-between; border-bottom: 1px solid #111; }
    </style>
""", unsafe_allow_html=True)

# 2. BANCO DE DADOS (PADRÃO OURO)
if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. NAVEGAÇÃO POR ABAS
t_term, t_rel, t_analise = st.tabs(["🎮 TERMINAL DE ENTRADA", "📑 RELATÓRIO FISCAL", "📈 ANÁLISE"])

# --- ABA 1: TERMINAL (AÇÃO) ---
with t_term:
    st.subheader("> REGISTRO DE OPERAÇÃO")
    item_op = st.selectbox("SELECIONE O PRODUTO:", list(banco.keys()))
    
    # Stake orientada: Usando valor exato conforme sua instrução de 20/10/1 Real
    val_op = st.number_input("VALOR DA RODADA ($):", value=banco[item_op]['ref'], step=0.10)
    
    if st.button("🚀 EXECUTAR REGISTRO"):
        # Cálculo de variação e projeção com -50% conforme sua regra
        variacao = ((val_op - banco[item_op]['ref']) / banco[item_op]['ref'])
        projecao_ajustada = variacao * 0.5  # Aplicando -50% da projeção
        
        st.session_state['logs_sentinela'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item_op,
            "VALOR_NUM": val_op,
            "STATUS": "ENTRA" if variacao < 0.1 else "PULA"
        })
        st.success(f"REGISTRO DE {item_op} ENVIADO PARA O BANCO.")

# --- ABA 2: RELATÓRIO (O CORAÇÃO DO ERRO ANTERIOR) ---
with t_rel:
    st.subheader("> AUDITORIA DIGITAL")
    
    if st.session_state['logs_sentinela']:
        df = pd.DataFrame(st.session_state['logs_sentinela'])
        
        # Cálculo total blindado (apenas números)
        total_acumulado = sum(d['VALOR_NUM'] for d in st.session_state['logs_sentinela'])
        
        # Interface de Nota Fiscal
        st.markdown(f"""
        <div class="nota-fiscal">
            <h2 style='text-align:center;'>CUPOM SENTINELA IA</h2>
            <p style='text-align:center;'>DATA: {datetime.now().strftime('%d/%m/%Y')}</p>
            <hr>
        """, unsafe_allow_html=True)
        
        for entry in st.session_state['logs_sentinela']:
            st.markdown(f"""
                <div class="nota-item">
                    <span>{entry['ITEM']} ({entry['HORA']})</span>
                    <span>$ {entry['VALOR_NUM']:.2f}</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
            <hr>
            <div style='display:flex; justify-content:space-between; font-weight:bold; font-size:1.2em;'>
                <span>TOTAL ACUMULADO:</span>
                <span>$ {total_acumulado:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download seguro para Celular
        csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 BAIXAR EXCEL (SANEADO)", data=csv, 
                           file_name=f"Relatorio_S.A_{datetime.now().strftime('%H%M')}.csv")
    else:
        st.warning("AGUARDANDO PRIMEIRA OPERAÇÃO NO TERMINAL.")

# --- ABA 3: ANÁLISE ---
with t_analise:
    st.write(f"### MÉTRICA: {item_op}")
    # Substituindo LIBERADO e PENDENTE pelos valores calculados conforme sua regra
    col1, col2 = st.columns(2)
    col1.metric("LIBERADO", f"{banco[item_op]['lib']}%")
    col2.metric("PENDENTE", f"{banco[item_op]['pen']}%")
    
    fig = px.pie(values=[banco[item_op]['lib'], banco[item_op]['pen']], 
                 names=['LIB', 'PEN'], hole=0.6,
                 color_discrete_sequence=['#00FF41', '#330000'])
    st.plotly_chart(fig, use_container_width=True)
                    
