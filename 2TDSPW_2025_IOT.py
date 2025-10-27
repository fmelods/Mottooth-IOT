import streamlit as st
import pandas as pd
import plotly.express as px
import time
from mottu_api import MottoAPI

# =========================================================
# CONFIGURAÇÃO BÁSICA
# =========================================================
st.set_page_config(page_title="MOTTU - IoT Dashboard Integrado",
                   layout="wide", page_icon="🛵")

# =========================================================
# SIDEBAR - LOGIN E CONFIGURAÇÃO
# =========================================================
st.sidebar.header("⚙️ Configurações da API")

if "api_url" not in st.session_state:
    st.session_state["api_url"] = "https://mottooth-java-1.onrender.com"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

api_url = st.sidebar.text_input("URL da API", value=st.session_state["api_url"])
username = st.sidebar.text_input("Usuário", value="admin@ex.com")
password = st.sidebar.text_input("Senha", type="password", value="fiap25")
intervalo = st.sidebar.slider("⏱️ Intervalo de atualização (s)", 5, 60, 5)

api = MottoAPI(api_url)

# Login / Logout
if not st.session_state["logged_in"]:
    if st.sidebar.button("🔐 Login"):
        if api.login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["api"] = api
            st.session_state["api_url"] = api_url
            st.success("✅ Login realizado!")
            st.rerun()
        else:
            st.error("Falha no login. Verifique usuário e senha.")
else:
    if st.sidebar.button("🚪 Sair"):
        st.session_state.clear()
        st.success("Logout realizado.")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("As variáveis podem ser armazenadas em `.streamlit/secrets.toml`.")

# =========================================================
# CONTEÚDO PRINCIPAL
# =========================================================
st.title("🛵 MOTTU - IoT Dashboard Integrado")
st.caption("Sprint 4 - Integração IoT + API Java + Banco Oracle")

if not st.session_state.get("logged_in"):
    st.warning("🔑 Faça login para visualizar os dados.")
    st.stop()

# =========================================================
# BUSCA DE DADOS
# =========================================================
api = st.session_state["api"]

try:
    motos = api.get_motos()
    beacons = api.get_beacons()
    localizacoes = api.get_localizacoes()
    online = True
except Exception as e:
    st.error(f"Erro ao buscar dados da API: {e}")
    motos = beacons = localizacoes = []
    online = False

# =========================================================
# MÉTRICAS SUPERIORES
# =========================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Motos", len(motos))
col2.metric("Beacons", len(beacons))
col3.metric("Localizações", len(localizacoes))
col4.metric("Status", "Online 🟢" if online else "Offline 🔴")

# =========================================================
# MAPA DAS MOTOS (com quadrantes visuais)
# =========================================================
st.subheader("📍 Localização das motos")

df_loc = pd.DataFrame()
if localizacoes:
    if isinstance(localizacoes, dict):
        if "content" in localizacoes and isinstance(localizacoes["content"], list):
            df_loc = pd.DataFrame(localizacoes["content"])
        else:
            df_loc = pd.DataFrame([localizacoes])
    elif isinstance(localizacoes, list):
        df_loc = pd.DataFrame(localizacoes)

if not df_loc.empty and {"posicaoX", "posicaoY"}.issubset(df_loc.columns):
    import plotly.graph_objects as go

    fig = go.Figure()

    # === ÁREAS DO PÁTIO ===
    areas = [
        {"nome": "Área A", "x0": 0, "x1": 50, "y0": 0, "y1": 350, "cor": "rgba(0, 128, 255, 0.2)"},
        {"nome": "Área B", "x0": 50, "x1": 100, "y0": 0, "y1": 350, "cor": "rgba(0, 255, 128, 0.2)"},
        {"nome": "Área C", "x0": 0, "x1": 50, "y0": 350, "y1": 700, "cor": "rgba(255, 255, 128, 0.2)"},
        {"nome": "Área D", "x0": 50, "x1": 100, "y0": 350, "y1": 700, "cor": "rgba(255, 128, 128, 0.2)"},
    ]

    for area in areas:
        fig.add_shape(
            type="rect",
            x0=area["x0"],
            x1=area["x1"],
            y0=area["y0"],
            y1=area["y1"],
            fillcolor=area["cor"],
            line=dict(width=0),
            layer="below"
        )
        fig.add_annotation(
            x=(area["x0"] + area["x1"]) / 2,
            y=(area["y0"] + area["y1"]) / 2,
            text=area["nome"],
            showarrow=False,
            font=dict(size=16, color="white")
        )

    # === PONTOS DAS MOTOS ===
    fig.add_trace(go.Scatter(
        x=df_loc["posicaoX"],
        y=df_loc["posicaoY"],
        mode="markers+text",
        text=df_loc.get("idMoto", df_loc.get("id", "")),
        textposition="top center",
        marker=dict(size=10, color="blue", line=dict(width=1, color="white")),
        name="Motos"
    ))

    fig.update_layout(
        title="🗺️ Mapa do Pátio (Áreas A, B, C e D)",
        xaxis_title="Posição X",
        yaxis_title="Posição Y",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font_color="white",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sem dados de localização ou formato incorreto.")

# =========================================================
# TABELAS DETALHADAS
# =========================================================
st.subheader("📋 Tabelas de Dados")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### 🏍️ Motos")
    if motos:
        st.dataframe(pd.DataFrame(motos))
    else:
        st.warning("Nenhuma moto cadastrada.")

with c2:
    st.markdown("#### 📡 Beacons")
    if beacons:
        st.dataframe(pd.DataFrame(beacons))
    else:
        st.warning("Nenhum beacon registrado.")

with c3:
    st.markdown("#### 📍 Localizações")
    if not df_loc.empty:
        st.dataframe(df_loc)
    else:
        st.warning("Sem dados de localização.")

# =========================================================
# ATUALIZAÇÃO AUTOMÁTICA
# =========================================================
st.markdown("---")
st.caption(f"🔁 Atualizando automaticamente a cada {intervalo} segundos...")
time.sleep(intervalo)
st.rerun()
