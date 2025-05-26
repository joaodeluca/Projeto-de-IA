import streamlit as st
import pandas as pd
import openai
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# ========== SEGURANÇA: API KEY NO .env ==========
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("API KEY da OpenAI não encontrada no .env!")
client = openai.OpenAI(api_key=openai_api_key)

st.set_page_config(
    page_title="S&P 500 Insights",
    layout="wide",
    page_icon="📊"
)

@st.cache_data
def load_data():
    df = pd.read_csv('constituents-financials_csv.csv')
    df.columns = [c.replace('/', '_').replace(' ', '_') for c in df.columns]
    return df

df = load_data()

# ======= HEADER =======
st.markdown("""
    <div style='background: linear-gradient(90deg, #23272f 0%, #4F8BF9 100%); padding: 1.5rem 2rem; border-radius: 14px; margin-bottom:1rem'>
        <h1 style='color:#fff; margin:0; font-size:2.5rem; font-weight:800;'>📊 S&P 500 Insights</h1>
        <p style='color:#e6e6e6; font-size:1.1rem; margin:0.3rem 0 0 0;'>Dashboard interativo, comparação de empresas e análise de investimentos com apoio de Inteligência Artificial</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ======= SIDEBAR =======
st.sidebar.markdown("<h2 style='color:#4F8BF9;'>Filtros</h2>", unsafe_allow_html=True)
setores = sorted(df['Sector'].dropna().unique())
setor = st.sidebar.selectbox("Setor", setores)
empresas = df[df['Sector'] == setor]['Name'].tolist()
empresa = st.sidebar.selectbox("Empresa", empresas)

df_setor = df[df['Sector'] == setor].copy()
df_empresa = df_setor[df_setor['Name'] == empresa].copy()

# ======= ABAS =======
tab1, tab2, tab3 = st.tabs([
    "🌐 Visão Geral do Setor",
    "🏢 Empresa Selecionada (SWOT IA)",
    "⚖️ Comparação de Empresas"
])

# ========== COLUNAS COM NOMES LEGÍVEIS PARA EXIBIÇÃO ==========
colunas_legiveis = {
    "Symbol": "Ticker",
    "Name": "Empresa",
    "Sector": "Setor",
    "Price": "Preço",
    "Price_Earnings": "P/L (Price/Earnings)",
    "Dividend_Yield": "Dividend Yield",
    "Earnings_Share": "Earnings/Share",
    "52_Week_Low": "52 Week Low",
    "52_Week_High": "52 Week High",
    "Market_Cap": "Market Cap",
    "EBITDA": "EBITDA",
    "Price_Sales": "Price/Sales",
    "Price_Book": "Price/Book",
    "SEC_Filings": "SEC Filings"
}

# ======= ABA 1: VISÃO GERAL DO SETOR =======
with tab1:
    st.markdown("<h2 style='color:#4F8BF9;'>Visão Geral do Setor</h2>", unsafe_allow_html=True)
    st.write(f"Setor selecionado: **{setor}**")
    st.divider()

    # Métricas principais em cards destacados
    kpis = {
        "Média Price/Earnings": f"{df_setor['Price_Earnings'].mean():.2f}",
        "Maior Market Cap": f"{df_setor['Market_Cap'].max()/1e9:.1f} Bi",
        "Média Dividend Yield": f"{df_setor['Dividend_Yield'].mean():.2f}"
    }
    col1, col2, col3 = st.columns(3)
    for idx, (k, v) in enumerate(kpis.items()):
        [col1, col2, col3][idx].markdown(
            f"<div style='background:#181c22; padding:1.2rem 0.8rem; border-radius:14px; text-align:center;'>"
            f"<span style='color:#4F8BF9; font-size:1.6rem; font-weight:bold;'>{v}</span><br>"
            f"<span style='color:#eee'>{k}</span></div>", unsafe_allow_html=True)

    # Filtra outliers para P/E
    filtered_df = df_setor[(df_setor['Price_Earnings'] > 0) & (df_setor['Price_Earnings'] < df_setor['Price_Earnings'].quantile(0.98))]

    # Histograma Price/Earnings
    st.markdown("#### Distribuição de Price/Earnings")
    pe_hist = px.histogram(
        filtered_df, x="Price_Earnings", nbins=20,
        color_discrete_sequence=["#4F8BF9"],
        labels={"Price_Earnings": "Price/Earnings"},
        template="plotly_dark"
    )
    pe_hist.update_traces(hovertemplate='P/E: %{x}<br>Empresas: %{y}')
    pe_hist.update_layout(
        plot_bgcolor="#181c22", paper_bgcolor="#181c22", font_color="#e6e6e6",
        height=340
    )
    st.plotly_chart(pe_hist, use_container_width=True)

    # Top 10 Market Cap
    st.markdown("#### Top 10 Empresas por Market Cap")
    top_mc = df_setor.sort_values('Market_Cap', ascending=False).head(10)
    bar_mc = px.bar(
        top_mc, x="Market_Cap", y="Name", orientation="h",
        color="Market_Cap", color_continuous_scale="blues",
        labels={"Market_Cap": "Market Cap (USD)", "Name": "Empresa"},
        template="plotly_dark",
        height=350
    )
    bar_mc.update_layout(yaxis={'categoryorder': 'total ascending'}, plot_bgcolor="#181c22", paper_bgcolor="#181c22")
    st.plotly_chart(bar_mc, use_container_width=True)

    st.markdown("#### Top 10 Dividend Yield")
    top_dy = df_setor.sort_values('Dividend_Yield', ascending=False).head(10)
    st.dataframe(
        top_dy[['Name', 'Dividend_Yield', 'Market_Cap']].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

# ======= ABA 2: EMPRESA SELECIONADA (SWOT IA) =======
with tab2:
    st.markdown(f"<h2 style='color:#58B368;'>Análise Completa da Empresa: {empresa}</h2>", unsafe_allow_html=True)
    st.divider()

    # KPIs principais
    pe_empresa = df_empresa['Price_Earnings'].values[0]
    mc_empresa = df_empresa['Market_Cap'].values[0]
    dy_empresa = df_empresa['Dividend_Yield'].values[0]
    pe_setor = df_setor['Price_Earnings'].mean()
    mc_setor = df_setor['Market_Cap'].mean()
    dy_setor = df_setor['Dividend_Yield'].mean()
    cards = [
        ("Price/Earnings", f"{pe_empresa:.2f}", f"{pe_empresa - pe_setor:+.2f} vs setor"),
        ("Market Cap", f"{mc_empresa/1e9:.2f} Bi", f"{mc_empresa - mc_setor:+.2e}"),
        ("Dividend Yield", f"{dy_empresa:.2f}", f"{dy_empresa - dy_setor:+.2f} vs setor"),
    ]
    cols = st.columns(3)
    for i, (label, val, delta) in enumerate(cards):
        cols[i].markdown(
            f"<div style='background:#181c22; padding:1.1rem 0.7rem; border-radius:14px; text-align:center;'>"
            f"<span style='color:#58B368; font-size:1.5rem; font-weight:bold;'>{val}</span><br>"
            f"<span style='color:#eee'>{label}</span><br>"
            f"<span style='color: #F97E4F; font-size:0.95rem;'>{delta}</span></div>", unsafe_allow_html=True)

    # Tabela de indicadores completos, com nomes legíveis
    st.markdown("#### Indicadores completos da empresa")
    dados_empresa = df_empresa.iloc[0]
    dados_exibir = []
    for col, label in colunas_legiveis.items():
        if col in dados_empresa:
            val = dados_empresa[col]
            # Formatação amigável para números grandes
            if isinstance(val, (int, float)):
                if abs(val) > 1e9:
                    val = f"{val:,.2f}"
                elif abs(val) > 1e6:
                    val = f"{val:,.1f}"
                elif abs(val) > 1e3:
                    val = f"{val:,.2f}"
                else:
                    val = f"{val}"
            dados_exibir.append({"Indicador": label, "Valor": val})
    st.table(pd.DataFrame(dados_exibir))

    st.markdown("---")
    st.subheader("Análise SWOT e Recomendações da IA")
    if 'ia_cache_swot' not in st.session_state:
        st.session_state['ia_cache_swot'] = {}
    chave = f"{empresa}_{setor}"

    if st.button("Gerar análise SWOT IA desta empresa"):
        prompt = (
            f"Faça uma análise SWOT (Forças, Fraquezas, Oportunidades, Ameaças) da empresa {empresa} do setor {setor} considerando:\n"
            f"- Price/Earnings: {pe_empresa}\n"
            f"- EBITDA: {df_empresa['EBITDA'].values[0]}\n"
            f"- Dividend Yield: {dy_empresa}\n"
            f"- Market Cap: {mc_empresa}\n"
            f"- Outros indicadores financeiros relevantes.\n"
            "Inclua recomendações de investimento, alertas de risco e possíveis estratégias para investidores."
        )
        with st.spinner("Chamando ChatGPT..."):
            try:
                resposta = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=0.7,
                )
                resumo = resposta.choices[0].message.content.strip()
                st.session_state['ia_cache_swot'][chave] = resumo
                st.success("Análise SWOT gerada!")
            except Exception as e:
                resumo = f"Erro: {e}"
                st.error(resumo)
    else:
        resumo = st.session_state['ia_cache_swot'].get(chave, "")

    if resumo:
        with st.expander("Ver análise completa da IA", expanded=True):
            st.markdown(f"<div style='color:#ddd; font-size:1.05rem;'>{resumo.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
    else:
        st.caption("Clique acima para gerar uma análise SWOT com IA para esta empresa.")

# ======= ABA 3: COMPARAÇÃO DE EMPRESAS =======
with tab3:
    st.markdown("<h2 style='color:#F97E4F;'>Comparação de Empresas do Setor</h2>", unsafe_allow_html=True)
    st.divider()
    empresa_a = st.selectbox("Empresa A", empresas, key="empresa_a")
    empresas_b = [e for e in empresas if e != empresa_a]
    empresa_b = st.selectbox("Empresa B", empresas_b, key="empresa_b")

    df_a = df_setor[df_setor['Name'] == empresa_a].iloc[0]
    df_b = df_setor[df_setor['Name'] == empresa_b].iloc[0]

    st.markdown(f"<h4 style='color:#fff'><b>{empresa_a}</b> <span style='color:#aaa;font-size:1.3rem;'>&nbsp;vs&nbsp;</span> <b>{empresa_b}</b></h4>", unsafe_allow_html=True)

    # Indicadores para comparação (divididos por escala)
    indicadores_grandes = ['Market_Cap', 'EBITDA']
    indicadores_pequenos = ['Price_Earnings', 'Dividend_Yield']
    a_vals_grandes = [df_a[x] for x in indicadores_grandes]
    b_vals_grandes = [df_b[x] for x in indicadores_grandes]
    a_vals_pequenos = [df_a[x] for x in indicadores_pequenos]
    b_vals_pequenos = [df_b[x] for x in indicadores_pequenos]

    # Gráfico para indicadores grandes
    st.markdown("##### Indicadores Financeiros (Market Cap, EBITDA)")
    barras_fig_grandes = go.Figure(data=[
        go.Bar(
            y=indicadores_grandes, x=a_vals_grandes,
            orientation='h', name=empresa_a, marker_color="#4F8BF9"
        ),
        go.Bar(
            y=indicadores_grandes, x=b_vals_grandes,
            orientation='h', name=empresa_b, marker_color="#F97E4F"
        )
    ])
    barras_fig_grandes.update_layout(
        barmode='group', template="plotly_dark", height=220,
        plot_bgcolor="#181c22", paper_bgcolor="#181c22",
        font_color="#e6e6e6"
    )
    st.plotly_chart(barras_fig_grandes, use_container_width=True)

    # Gráfico para indicadores pequenos
    st.markdown("##### Indicadores Proporcionais (P/L, Dividend Yield)")
    barras_fig_pequenos = go.Figure(data=[
        go.Bar(
            y=indicadores_pequenos, x=a_vals_pequenos,
            orientation='h', name=empresa_a, marker_color="#4F8BF9"
        ),
        go.Bar(
            y=indicadores_pequenos, x=b_vals_pequenos,
            orientation='h', name=empresa_b, marker_color="#F97E4F"
        )
    ])
    barras_fig_pequenos.update_layout(
        barmode='group', template="plotly_dark", height=220,
        plot_bgcolor="#181c22", paper_bgcolor="#181c22",
        font_color="#e6e6e6"
    )
    st.plotly_chart(barras_fig_pequenos, use_container_width=True)

    # Cards comparativos abaixo dos gráficos
    todos_indicadores = indicadores_grandes + indicadores_pequenos
    a_vals_all = [df_a[x] for x in todos_indicadores]
    b_vals_all = [df_b[x] for x in todos_indicadores]
    cols = st.columns(4)
    for i, ind in enumerate(todos_indicadores):
        cols[i % 4].markdown(
            f"<div style='background:#181c22; padding:1rem 0.7rem; border-radius:14px; text-align:center;'>"
            f"<span style='color:#4F8BF9; font-size:1.15rem; font-weight:bold;'>{a_vals_all[i]:,.2f}</span>"
            f"<br><span style='color:#eee'>{ind} ({empresa_a})</span>"
            "</div>"
            "<div style='background:#181c22; margin-top:0.7rem; padding:1rem 0.7rem; border-radius:14px; text-align:center;'>"
            f"<span style='color:#F97E4F; font-size:1.15rem; font-weight:bold;'>{b_vals_all[i]:,.2f}</span>"
            f"<br><span style='color:#eee'>{ind} ({empresa_b})</span>"
            "</div>", unsafe_allow_html=True)

    # Botão IA: comparação
    if 'ia_cache_comp' not in st.session_state:
        st.session_state['ia_cache_comp'] = {}
    comp_key = f"{empresa_a}_VS_{empresa_b}_{setor}"

    if st.button(f"Análise IA: {empresa_a} vs {empresa_b}"):
        prompt = (
            f"Compare as empresas {empresa_a} e {empresa_b}, ambas do setor {setor}, considerando seus principais indicadores:\n"
            f"{empresa_a} - Price/Earnings: {df_a['Price_Earnings']}, EBITDA: {df_a['EBITDA']}, Market Cap: {df_a['Market_Cap']}, Dividend Yield: {df_a['Dividend_Yield']}.\n"
            f"{empresa_b} - Price/Earnings: {df_b['Price_Earnings']}, EBITDA: {df_b['EBITDA']}, Market Cap: {df_b['Market_Cap']}, Dividend Yield: {df_b['Dividend_Yield']}.\n"
            "Faça uma análise comparativa detalhada, indique pontos fortes e fracos de cada empresa, e qual seria mais indicada para investimento considerando diferentes perfis de risco."
        )
        with st.spinner("Chamando IA..."):
            try:
                resposta = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=0.7,
                )
                analise = resposta.choices[0].message.content.strip()
                st.session_state['ia_cache_comp'][comp_key] = analise
                st.success("Análise comparativa gerada!")
            except Exception as e:
                analise = f"Erro: {e}"
                st.error(analise)
    else:
        analise = st.session_state['ia_cache_comp'].get(comp_key, "")

    if analise:
        with st.expander("Ver análise completa da IA", expanded=True):
            st.markdown(f"<div style='color:#ddd; font-size:1.05rem;'>{analise.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
    else:
        st.caption("Selecione as empresas e clique para gerar uma análise IA da comparação.")

# ======= RODAPÉ E CRÉDITOS =======
st.markdown("<hr style='margin-top:2rem; margin-bottom:1rem; border:1px solid #2f3136'>", unsafe_allow_html=True)
st.markdown("<div style='color:#7fa6ee; text-align:center'>Projeto IA Mackenzie 2025 &bull; Daniel, Gustavo, João Victor</div>", unsafe_allow_html=True)
