import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. CONFIGURAÇÃO KIT RUBI
st.set_page_config(page_title="IA-SENTINELA | Auditoria", layout="wide")

def emitir_bip():
    bip_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(bip_html, height=0)

if 'historico_dia' not in st.session_state:
    st.session_state['historico_dia'] = []

# 2. BANCO DE DADOS (Nomes internos sem acento para o Excel ler perfeito)
banco = {
    'Salmao':   {'ref': 8.50,  'liberado': 85, 'pendente': 15},
    'Camarao':  {'ref': 13.00, 'liberado': 60, 'pendente': 40},
    'Tilapia':  {'ref': 5.40,  'liberado': 95, 'pendente': 5}
}

# 3. INTERFACE EM ABAS
aba_config, aba_dashboard, aba_consolidado, aba_relatorio = st.tabs([
    "⚙️ Configuracao", "📈 Dashboard", "📊 Visao Consolidada", "📂 Relatorios"
])

with aba_config:
    st.subheader("Entrada de Dados")
    peixe_sel = st.selectbox("Selecione o Pescado:", list(banco.keys()))
    preco_atual = st.number_input(f"Preco Atual {peixe_sel} (USD/KG):", value=banco[peixe_sel]['ref'])
    
    dados = banco[peixe_sel]
    x_calc = ((preco_atual - dados['ref']) / dados['ref']) * 100
    
    if preco_atual == 1.0: veredito_txt = "VACUO"
    elif x_calc >= 10: veredito_txt = "PULA"
    else: veredito_txt = "ENTRA"

    if st.button("🔔 Registrar Aumento"):
        st.session_state['historico_dia'].insert(0, {
            "Horario": datetime.now().strftime("%H:%M:%S"),
            "Produto": peixe_sel,
            "Preco": f"USD {preco_atual:.2f}",
            "Variacao_X": f"{x_calc:.2f}%",
            "Veredito": veredito_txt
        })
        st.success("Registrado com sucesso!")

with aba_dashboard:
    st.title(f"🛡️ Sentinela: {peixe_sel}")
    if preco_atual == 1.0 or x_calc >= 10: emitir_bip()
    st.metric("LIBERADO", f"{dados['liberado']}%")
    st.metric("PENDENTE", f"{dados['pendente']}%")
    st.info(f"Veredito Atual: {veredito_txt}")
    
    fig_ind = px.pie(values=[dados['liberado'], dados['pendente']], names=['LIBERADO', 'PENDENTE'], hole=0.5, color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig_ind, use_container_width=True)

with aba_consolidado:
    st.subheader("📊 O Casado (Panorama Geral)")
    
    # --- O GRÁFICO QUE TINHA SUMIDO (RESTAURADO) ---
    df_graph = pd.DataFrame([
        {"Pescado": k, "Status": "Liberado", "Valor": v['liberado']} for k, v in banco.items()
    ] + [
        {"Pescado": k, "Status": "Pendente", "Valor": v['pendente']} for k, v in banco.items()
    ])
    
    fig_cons = px.bar(df_graph, x="Pescado", y="Valor", color="Status",
                      barmode="stack",
                      color_discrete_map={"Liberado": "#2ecc71", "Pendente": "#e74c3c"})
    st.plotly_chart(fig_cons, use_container_width=True)
    
    # Tabela consolidada abaixo do gráfico
    df_visual = pd.DataFrame([{"Pescado": k, "Ref. Mercado": f"USD {v['ref']:.2f}", "Liberado": f"{v['liberado']}%", "Pendente": f"{v['pendente']}%"} for k, v in banco.items()])
    st.table(df_visual)

with aba_relatorio:
    st.subheader("📂 Relatorios de Auditoria")
    if st.session_state['historico_dia']:
        df_relatorio = pd.DataFrame(st.session_state['historico_dia'])
        st.table(df_relatorio)
        
        # Download sem erros de acento (Padrão Excel)
        csv = df_relatorio.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(label="📥 Baixar Relatorio Excel", data=csv, file_name=f"auditoria_{datetime.now().strftime('%d_%m_%Y')}.csv", mime="text/csv")
    else:
        st.info("Nenhum registro para exibir.")
    
