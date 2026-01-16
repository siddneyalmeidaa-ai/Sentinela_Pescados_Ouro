import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. CONFIGURAÇÃO KIT RUBI
st.set_page_config(page_title="IA-SENTINELA | Auditoria", layout="wide")

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

# Inicializar o histórico na memória do navegador (Relatório do Dia)
if 'historico_dia' not in st.session_state:
    st.session_state['historico_dia'] = []

# 2. BANCO DE DADOS
banco = {
    'Salmão':   {'ref': 8.50,  'liberado': 85, 'pendente': 15},
    'Camarão':  {'ref': 13.00, 'liberado': 60, 'pendente': 40},
    'Tilápia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5}
}

# 3. INTERFACE EM ABAS
aba_config, aba_dashboard, aba_consolidado, aba_relatorio = st.tabs([
    "⚙️ Configuração", 
    "📈 Dashboard", 
    "📊 Visão Consolidada", 
    "📂 Relatórios do Dia"
])

with aba_config:
    st.subheader("Entrada de Dados")
    peixe_sel = st.selectbox("Selecione o Pescado:", list(banco.keys()))
    preco_atual = st.number_input(f"Preço Atual {peixe_sel} (USD/KG):", value=banco[peixe_sel]['ref'])
    
    if st.button("🔔 Registrar e Auditar"):
        dados = banco[peixe_sel]
        # Cálculo do X com a regra de proteção
        x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
        
        # Veredito
        if preco_atual == 1.0: veredito = "VÁCUO"; cor = "🔴"
        elif x_calc >= 10: veredito = "PULA"; cor = "🟡"
        else: veredito = "ENTRA"; cor = "🟢"
        
        # Salvar no Relatório do Dia
        novo_registro = {
            "Horário": datetime.now().strftime("%H:%M:%S"),
            "Produto": peixe_sel,
            "Preço Informado": f"USD {preco_atual:.2f}",
            "Variação X": f"{x_calc:.2f}%",
            "Veredito": f"{cor} {veredito}"
        }
        st.session_state['historico_dia'].insert(0, novo_registro)
        st.success("Registro enviado para Auditoria!")

# Lógica para exibição nas abas
dados = banco[peixe_sel]
x_atual = ((preco_atual - dados['ref']) / dados['ref']) * 100

with aba_dashboard:
    st.title(f"🛡️ Sentinela: {peixe_sel}")
    if preco_atual == 1.0 or x_atual >= 10: emitir_bip()
    st.metric("LIBERADO", f"{dados['liberado']}%")
    st.metric("PENDENTE", f"{dados['pendente']}%")

with aba_consolidado:
    st.subheader("📊 O Casado (Panorama Geral)")
    df_visual = pd.DataFrame([{
        "Pescado": k, "Ref. Mercado": f"USD {v['ref']:.2f}", 
        "Liberado": f"{v['liberado']}%", "Pendente": f"{v['pendente']}%"
    } for k, v in banco.items()])
    st.table(df_visual)

# --- NOVA ABA: RELATÓRIOS DO DIA ---
with aba_relatorio:
    st.subheader("📂 Base de Relatórios (Histórico de Aumento do Dia)")
    if st.session_state['historico_dia']:
        df_relatorio = pd.DataFrame(st.session_state['historico_dia'])
        st.dataframe(df_relatorio, use_container_width=True)
        
        # Botão de download configurado para celular
        csv = df_relatorio.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 Baixar Relatório do Dia", csv, "relatorio_dia.csv", "text/csv")
    else:
        st.info("Nenhuma movimentação registrada hoje.")
        
