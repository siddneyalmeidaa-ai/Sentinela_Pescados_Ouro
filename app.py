import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. SETUP DE SEGURANÇA (ESTRUTURA SIMPLIFICADA)
st.set_page_config(page_title="SENTINELA S.A.", layout="wide")

# Limpeza automática de lixo de memória para evitar o KeyError das imagens
if 'logs_sentinela' not in st.session_state:
    st.session_state['logs_sentinela'] = []

# Botão na lateral para resetar se a tela ficar vermelha
if st.sidebar.button("RESETAR SISTEMA"):
    st.session_state['logs_sentinela'] = []
    st.rerun()

# 2. BANCO DE DADOS
banco = {
    'Salmão':   {'ref': 8.50,  'lib': 85, 'pen': 15},
    'Camarão':  {'ref': 13.00, 'lib': 60, 'pen': 40},
    'Tilápia':  {'ref': 5.40,  'lib': 95, 'pen': 5}
}

# 3. ESTILO (APENAS O ESSENCIAL)
st.markdown("<style>.stApp{background-color:#000;color:#0F0;}</style>", unsafe_allow_html=True)

# 4. NAVEGAÇÃO
t1, t2, t3 = st.tabs(["🎮 ENTRADA", "📑 RELATÓRIO", "📊 MÉTRICAS"])

with t1:
    st.write("### REGISTRO")
    item = st.selectbox("PRODUTO:", list(banco.keys()))
    valor = st.number_input("VALOR ATUAL:", value=banco[item]['ref'], step=0.10)
    
    if st.button("EXECUTAR"):
        # Regra de variação
        var = ((valor - banco[item]['ref']) / banco[item][ 'ref'])
        st.session_state['logs_sentinela'].insert(0, {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ITEM": item,
            "VALOR_NUM": float(valor),
            "VAR": f"{var:.2%}",
            "STATUS": "ENTRA" if var < 0.1 else "PULA"
        })
        st.success("SALVO!")

with t2:
    st.write("### AUDITORIA")
    if st.session_state['logs_sentinela']:
        df = pd.DataFrame(st.session_state['logs_sentinela'])
        
        # SOMA BLINDADA (Ignora dados corrompidos das fotos antigas)
        total = sum(float(d.get('VALOR_NUM', 0)) for d in st.session_state['logs_sentinela'])
        
        st.dataframe(df, use_container_width=True)
        
        st.markdown(f"""
        ---
        **TOTAL ACUMULADO: $ {total:.2f}**
        ---
        """)
        
        csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("BAIXAR EXCEL", data=csv, file_name="relatorio.csv")
    else:
        st.info("SEM DADOS")

with t3:
    st.write(f"### ANÁLISE: {item}")
    l, p = banco[item]['lib'], banco[item]['pen']
    st.metric("LIBERADO", f"{l}%")
    fig = px.pie(values=[l, p], names=['LIB', 'PEN'], hole=0.7, color_discrete_sequence=['#0F0', '#300'])
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font_color="#0F0")
    st.plotly_chart(fig, use_container_width=True)
    
