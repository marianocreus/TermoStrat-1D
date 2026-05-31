"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Simulación de Estratificación Térmica de Termotanque Domiciliario          ║
║  Modelo Multi-Nodo Compatible con EnergyPlus WaterHeater:Stratified         ║
╚══════════════════════════════════════════════════════════════════════════════╝
Ejecutar:  streamlit run app_termotanque.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# Configuración de página
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Termotanque · Simulación Térmica",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS personalizado
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
  }

  /* Fondo general */
  .stApp { background-color: #0f1117; color: #e8eaf0; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141823 0%, #0e1420 100%);
    border-right: 1px solid #1e2740;
  }

  /* Header principal */
  .main-header {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2f4a 50%, #0d2137 100%);
    border: 1px solid #1e4060;
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
  }
  .main-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,120,40,0.12) 0%, transparent 70%);
    border-radius: 50%;
  }
  .main-header h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.7rem;
    font-weight: 600;
    color: #ff8c42;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
  }
  .main-header p {
    color: #8a9bb5;
    font-size: 0.92rem;
    margin: 0;
    font-weight: 300;
  }

  /* Tarjetas de métricas */
  .metric-card {
    background: #141c2e;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: center;
    transition: border-color 0.2s;
  }
  .metric-card:hover { border-color: #2e4a70; }
  .metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #ff8c42;
    display: block;
    margin-bottom: 4px;
  }
  .metric-label {
    font-size: 0.75rem;
    color: #5a7090;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .metric-unit {
    font-size: 0.78rem;
    color: #8a9bb5;
  }

  /* Sección de resultados */
  .results-section {
    background: #0d1520;
    border: 1px solid #1a2a40;
    border-left: 3px solid #ff8c42;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 14px 0;
  }
  .results-section h4 {
    font-family: 'IBM Plex Mono', monospace;
    color: #ff8c42;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 0 0 10px 0;
  }

  /* Badges de estado */
  .badge-ok   { background:#1a3a2a; color:#4caf50; border:1px solid #2d6040; border-radius:4px; padding:2px 8px; font-size:0.78rem; font-family:'IBM Plex Mono',monospace; }
  .badge-warn { background:#3a2a10; color:#ff9800; border:1px solid #6a4a20; border-radius:4px; padding:2px 8px; font-size:0.78rem; font-family:'IBM Plex Mono',monospace; }
  .badge-err  { background:#3a1a1a; color:#ef5350; border:1px solid #6a2a2a; border-radius:4px; padding:2px 8px; font-size:0.78rem; font-family:'IBM Plex Mono',monospace; }

  /* Tabla de balance */
  .balance-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid #1a2740;
    font-size: 0.88rem;
  }
  .balance-row:last-child { border-bottom: none; }
  .balance-key   { color: #8a9bb5; }
  .balance-value { font-family:'IBM Plex Mono',monospace; color:#e8eaf0; font-weight:600; }

  /* Título de sección */
  .section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    font-weight: 600;
    color: #4a7ab5;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 24px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e3050, transparent);
  }

  /* Estilo matplotlib para fondo oscuro */
  .stPlotlyChart, .element-container img { border-radius: 8px; }

  /* Botón principal */
  .stButton > button {
    background: linear-gradient(135deg, #e05a00, #ff8c42) !important;
    color: #0f1117 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
  }
  .stButton > button:hover { opacity: 0.88 !important; }

  /* Slider y number input */
  .stSlider > div > div > div > div { background: #ff8c42 !important; }
  [data-testid="stNumberInput"] input { background: #141c2e !important; color:#e8eaf0 !important; border-color:#1e3050 !important; }

  /* Expander */
  .streamlit-expanderHeader {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #4a7ab5 !important;
    background: #0d1520 !important;
  }
  [data-testid="stExpander"] { border: 1px solid #1a2740 !important; border-radius: 8px !important; }

  /* Tab */
  .stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #5a7090 !important;
  }
  .stTabs [aria-selected="true"] { color: #ff8c42 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Estilo matplotlib oscuro
# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0d1520",
    "axes.facecolor":    "#0d1520",
    "axes.edgecolor":    "#1e2d4a",
    "axes.labelcolor":   "#8a9bb5",
    "axes.titlecolor":   "#c0cce0",
    "text.color":        "#8a9bb5",
    "xtick.color":       "#5a7090",
    "ytick.color":       "#5a7090",
    "grid.color":        "#1a2740",
    "grid.alpha":        0.5,
    "figure.dpi":        130,
    "font.family":       "monospace",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.spines.left":  True,
    "axes.spines.bottom":True,
})

# ─────────────────────────────────────────────────────────────────────────────
# Funciones del modelo
# ─────────────────────────────────────────────────────────────────────────────
def construir_caudal_vector(eventos, n_pasos, dt_seg, rho_agua):
    caudal = np.zeros(n_pasos)
    etiquetas = [""] * n_pasos
    for (hora_ini, dur_min, q_lmin, desc) in eventos:
        t_ini_seg = hora_ini * 3600.0
        t_fin_seg = t_ini_seg + dur_min * 60.0
        paso_ini  = int(t_ini_seg / dt_seg)
        paso_fin  = int(t_fin_seg / dt_seg)
        for p in range(max(0, paso_ini), min(n_pasos, paso_fin)):
            if q_lmin > caudal[p]:
                caudal[p] = q_lmin
            etiquetas[p] = desc
    caudal_kg_s = caudal * rho_agua / (1000.0 * 60.0)
    return caudal_kg_s, etiquetas


def simular_termotanque(
    n_nodos, n_pasos, dt_seg,
    T_ini, T_amb, T_red,
    M_nodo, Cp, Rho,
    U_cond, U_conv, A_lat, A_tub, A_tapa,
    K_eff, V_NODO_M3,
    P_calef1, P_calef2, nodo_c1, nodo_c2,
    T_set, T_dead, nodo_sensor,
    C_inv, caudal_kg_s
):
    T      = np.full(n_nodos, T_ini, dtype=float)
    T_hist = np.zeros((n_pasos, n_nodos))
    Q_calef_v    = np.zeros(n_pasos)
    Q_perd_v     = np.zeros(n_pasos)
    Q_consumo_v  = np.zeros(n_pasos)
    estado_calef = np.zeros((n_pasos, 2), dtype=int)

    alpha_inv = min(0.5, C_inv * dt_seg / V_NODO_M3)
    T_ini_media = T_ini

    on_c1 = T[nodo_c1] < (T_set - T_dead)
    on_c2 = T[nodo_c2] < (T_set - T_dead)

    for paso in range(n_pasos):
        T_hist[paso] = T.copy()

        if T[nodo_sensor] >= T_set:
            on_c1 = False
        elif T[nodo_sensor] < (T_set - T_dead):
            on_c1 = True
        if T[nodo_sensor] >= T_set:
            on_c2 = False
        elif T[nodo_sensor] < (T_set - T_dead):
            on_c2 = True

        estado_calef[paso, 0] = int(on_c1)
        estado_calef[paso, 1] = int(on_c2)

        dT = np.zeros(n_nodos)
        q_perd_paso   = 0.0
        q_calef_real  = 0.0
        q_consumo_paso = 0.0

        for i in range(n_nodos):
            Aef_CON = A_lat
            if i == n_nodos - 1:
                Aef_CON += A_tapa
            q_perd_CON = U_cond * Aef_CON * (T[i] - T_amb)
            q_perd_paso += q_perd_CON

            Aef_SIN = A_tub
            if i == 0:
                Aef_SIN += A_tapa
            q_perd_SIN = U_conv * Aef_SIN * (T[i] - T_amb)
            q_perd_paso += q_perd_SIN

            q_cond_i = 0.0
            if i > 0:
                q_cond_i += K_eff * (T[i-1] - T[i])
            if i < n_nodos - 1:
                q_cond_i += K_eff * (T[i+1] - T[i])

            m_dot = caudal_kg_s[paso]
            if m_dot > 0:
                T_entrada_i = T_red if i == 0 else T[i-1]
                q_advec_i   = m_dot * Cp * (T_entrada_i - T[i])
                if i == n_nodos - 1:
                    q_consumo_paso += max(m_dot * Cp * (T[i] - T_red), 0.0)
            else:
                q_advec_i = 0.0

            P_tubo = 0.0
            if i == 0:
                P_tubo = 0
            elif i < n_nodos - 1:
                P_tubo = P_calef2 * (1/2)**i
            else:
                P_tubo = P_calef2 * (1/2)**(n_nodos - 2)

            q_calef_i = 0.0
            if i == nodo_c1 and on_c1:
                q_calef_i += P_calef1
            if on_c2:
                q_calef_i += P_tubo
            q_calef_real += q_calef_i

            dT[i] = (dt_seg / (M_nodo * Cp)) * (
                q_calef_i - q_perd_CON - q_perd_SIN + q_cond_i + q_advec_i
            )

        T = T + dT

        for i in range(n_nodos - 1):
            if T[i] > T[i+1]:
                T_mezcla = 0.5 * (T[i] + T[i+1])
                T[i]   = T[i]   + alpha_inv * (T_mezcla - T[i])
                T[i+1] = T[i+1] + alpha_inv * (T_mezcla - T[i+1])

        Q_calef_v[paso]   = q_calef_real
        Q_perd_v[paso]    = q_perd_paso
        Q_consumo_v[paso] = q_consumo_paso

    E_calef_kWh   = np.sum(Q_calef_v)   * dt_seg / 3_600_000.0
    E_perd_kWh    = np.sum(Q_perd_v)    * dt_seg / 3_600_000.0
    E_consumo_kWh = np.sum(Q_consumo_v) * dt_seg / 3_600_000.0
    M_total       = M_nodo * n_nodos
    delta_E_alm   = M_total * Cp * (T_hist[-1].mean() - T_ini_media) / 3_600_000.0

    return T_hist, Q_calef_v, Q_perd_v, E_calef_kWh, E_perd_kWh, estado_calef, E_consumo_kWh, delta_E_alm

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Parámetros
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px 0;'>
      <div style='font-family:IBM Plex Mono,monospace; font-size:1.1rem; font-weight:600; color:#ff8c42;'>⚙ PARÁMETROS</div>
      <div style='font-size:0.75rem; color:#4a6080; margin-top:4px;'>Configure la simulación</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Geometría ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Geometría del Tanque</div>", unsafe_allow_html=True)
    V_TOTAL_L  = st.number_input("Volumen total [L]",        min_value=30.0,  max_value=300.0, value=80.0,  step=5.0)
    H_TANQUE   = st.number_input("Altura total [m]",         min_value=0.4,   max_value=2.0,   value=0.627, step=0.01, format="%.3f")
    D_TANQUE   = st.number_input("Diámetro interior [m]",    min_value=0.15,  max_value=0.70,  value=0.410, step=0.01, format="%.3f")
    D_TUBO     = st.number_input("Diámetro tubo gases [m]",  min_value=0.03,  max_value=0.15,  value=0.075, step=0.005, format="%.3f")
    R_CASQUETE = st.number_input("Radio casquete [m]",       min_value=0.10,  max_value=0.50,  value=0.255, step=0.005, format="%.3f")
    H_CASQUETE = st.number_input("Altura casquete [m]",      min_value=0.04,  max_value=0.25,  value=0.104, step=0.005, format="%.3f")
    N_NODOS    = st.slider(       "Número de nodos",          min_value=3,     max_value=12,    value=11)

    # ── Calefactor ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Calefactor a Gas</div>", unsafe_allow_html=True)
    P_CALEFACTOR = st.number_input("Potencia útil [W]",     min_value=1000.0, max_value=10000.0, value=4800.0, step=100.0)
    T_SETPOINT   = st.slider("Setpoint [°C]",               min_value=40.0,   max_value=75.0,   value=60.0, step=1.0)
    T_DEADBAND   = st.slider("Banda muerta [°C]",           min_value=1.0,    max_value=10.0,   value=5.0,  step=0.5)

    # ── Aislamiento ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Aislamiento (PUR)</div>", unsafe_allow_html=True)
    E_AISLAMIENTO = st.number_input("Espesor [m]",         min_value=0.01, max_value=0.15, value=0.05, step=0.005, format="%.3f")
    K_AISLAMIENTO = st.number_input("Conductividad [W/mK]",min_value=0.02, max_value=0.06, value=0.034, step=0.001, format="%.3f")
    U_CONV        = st.number_input("U convección pared sin aisl [W/m²K]", min_value=2.0, max_value=25.0, value=7.5, step=0.5)

    # ── Condiciones ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Condiciones Iniciales</div>", unsafe_allow_html=True)
    T_INICIAL  = st.slider("T inicial [°C]",    min_value=5.0,  max_value=70.0, value=17.0, step=1.0)
    T_AMBIENTE = st.slider("T ambiente [°C]",   min_value=0.0,  max_value=40.0, value=15.0, step=1.0)
    T_RED      = st.slider("T agua de red [°C]",min_value=5.0,  max_value=30.0, value=17.0, step=1.0)

    # ── Simulación ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Simulación Temporal</div>", unsafe_allow_html=True)
    DT_SEG         = st.selectbox("Paso de tiempo [s]", [5, 10, 15, 30, 60], index=1)
    DURACION_HORAS = st.slider("Duración [h]",         min_value=6, max_value=48, value=25)
    C_INVERSION    = st.number_input("Coef. mezcla inversión [m³/s]", min_value=0.0001, max_value=0.1, value=0.001, step=0.0005, format="%.4f")

    # ── Propiedades agua ────────────────────────────────────────────────────
    with st.expander("Propiedades físicas del agua"):
        RHO_AGUA = st.number_input("Densidad [kg/m³]",       value=983.0, step=1.0)
        CP_AGUA  = st.number_input("Calor específico [J/kgK]", value=4185.0, step=10.0)
        K_AGUA   = st.number_input("Conductividad [W/mK]",   value=0.651, step=0.001, format="%.3f")

    # ── Perfil de consumo ────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Perfil de Consumo</div>", unsafe_allow_html=True)
    perfil_preset = st.selectbox(
        "Perfil predefinido",
        ["Sin consumo", "Familia 4 personas – Día típico", "Familia 4 personas – Uso intensivo", "Personalizado"],
        index=0
    )

    EVENTOS_CONSUMO_DEF = {
        "Sin consumo": [],
        "Familia 4 personas – Día típico": [
            (6.5,  8,  9.0, "Ducha – Persona 1"),
            (7.0,  8,  9.0, "Ducha – Persona 2"),
            (7.5,  3,  5.0, "Lavamanos mañana"),
            (7.8,  5,  3.0, "Cocina – desayuno"),
            (8.0,  8,  9.0, "Ducha – Persona 3"),
            (8.5,  8,  9.0, "Ducha – Persona 4"),
            (12.5, 4,  3.0, "Cocina – almuerzo"),
            (13.0, 3,  4.0, "Lavamanos mediodía"),
            (19.0, 4,  3.0, "Cocina – cena"),
            (19.5, 3,  4.0, "Lavamanos tarde"),
            (20.0,10,  9.0, "Ducha – Persona 1 (noche)"),
            (20.5,10,  9.0, "Ducha – Persona 2 (noche)"),
        ],
        "Familia 4 personas – Uso intensivo": [
            (6.0, 12, 10.0, "Ducha larga – P1"),
            (6.8, 12, 10.0, "Ducha larga – P2"),
            (7.5, 12, 10.0, "Ducha larga – P3"),
            (8.2, 12, 10.0, "Ducha larga – P4"),
            (12.5, 5,  4.0, "Cocina almuerzo"),
            (19.5, 5,  4.0, "Cocina cena"),
            (21.0, 12,  9.0, "Ducha noche – P1"),
            (21.8, 12,  9.0, "Ducha noche – P2"),
        ],
    }

    if perfil_preset == "Personalizado":
        st.info("Agregue eventos manualmente:")
        n_eventos = st.number_input("Cantidad de eventos", min_value=0, max_value=20, value=2, step=1)
        EVENTOS_CONSUMO = []
        for ev in range(int(n_eventos)):
            with st.expander(f"Evento {ev+1}"):
                hora = st.number_input(f"Hora inicio [h]",  min_value=0.0, max_value=23.9, value=float(6+ev), step=0.25, key=f"h{ev}")
                dur  = st.number_input(f"Duración [min]",   min_value=1,   max_value=120,  value=8, key=f"d{ev}")
                caud = st.number_input(f"Caudal [L/min]",   min_value=1.0, max_value=20.0, value=9.0, step=0.5, key=f"c{ev}")
                desc = st.text_input(  f"Descripción",      value=f"Evento {ev+1}", key=f"desc{ev}")
                EVENTOS_CONSUMO.append((hora, dur, caud, desc))
    else:
        EVENTOS_CONSUMO = EVENTOS_CONSUMO_DEF[perfil_preset]

    st.markdown("---")
    ejecutar = st.button("▶  EJECUTAR SIMULACIÓN")

# ─────────────────────────────────────────────────────────────────────────────
# CABECERA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='main-header'>
  <h1>🌡 TERMOTANQUE · ESTRATIFICACIÓN TÉRMICA</h1>
  <p>Simulación multi-nodo · Compatible con EnergyPlus <code>WaterHeater:Stratified</code> v26-1-0 &nbsp;|&nbsp; Modelo 1-DIM Euler Explícito</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULO DE PARÁMETROS DERIVADOS
# ─────────────────────────────────────────────────────────────────────────────
V_TOTAL_M3     = V_TOTAL_L / 1000.0
A_SEC_TANQ     = np.pi * (D_TANQUE/2)**2
P_TAN          = np.pi * D_TANQUE
A_SEC_TUBO     = np.pi * (D_TUBO/2)**2
P_TUB          = np.pi * D_TUBO
A_CASQUETE     = 2 * np.pi * R_CASQUETE * H_CASQUETE
H_NODO         = H_TANQUE / N_NODOS
V_NODO_M3      = V_TOTAL_M3 / N_NODOS
M_NODO         = RHO_AGUA * V_NODO_M3
A_LAT_TANQ_NODO= P_TAN * H_NODO
A_LAT_TUBO_NODO= P_TUB * H_NODO
A_SEC_NODO     = A_SEC_TANQ - A_SEC_TUBO
A_TAPA         = A_CASQUETE - A_SEC_TUBO
R_COND         = E_AISLAMIENTO / K_AISLAMIENTO
U_COND         = 1.0 / R_COND
K_EFF_NODOS    = K_AGUA * A_SEC_NODO / H_NODO
N_PASOS        = int(DURACION_HORAS * 3600 / DT_SEG)
t_vec          = np.arange(N_PASOS) * DT_SEG / 3600.0
NODO_SENSOR    = (N_NODOS - 1) // 2
FRACCION_1     = 1.0
P_CALEFACTOR_1 = FRACCION_1 * P_CALEFACTOR
P_CALEFACTOR_2 = (1 - FRACCION_1) * P_CALEFACTOR
NODO_CALEF_1   = 0
NODO_CALEF_2   = 1

# Fourier
Fo = K_AGUA * DT_SEG / (RHO_AGUA * CP_AGUA * H_NODO**2)
estable = Fo <= 0.5

# ─────────────────────────────────────────────────────────────────────────────
# PANEL DE PARÁMETROS DERIVADOS (siempre visible)
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("📐 Parámetros geométricos y derivados", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    items = [
        ("Altura nodo", f"{H_NODO*100:.1f} cm"),
        ("Vol. nodo",   f"{V_NODO_M3*1000:.2f} L"),
        ("Masa nodo",   f"{M_NODO:.2f} kg"),
        ("A sec. nodo", f"{A_SEC_NODO*1e4:.1f} cm²"),
        ("U_cond",      f"{U_COND:.3f} W/m²K"),
        ("K_eff nodos", f"{K_EFF_NODOS:.4f} W/K"),
        ("N° pasos",    f"{N_PASOS:,}"),
        ("Fourier Fo",  f"{Fo:.5f}"),
    ]
    cols = [c1, c2, c3, c4]
    for idx, (k, v) in enumerate(items):
        with cols[idx % 4]:
            color = "#4caf50" if (k == "Fourier Fo" and estable) else ("#ef5350" if k == "Fourier Fo" else "#ff8c42")
            st.markdown(f"""
            <div style='background:#0d1520;border:1px solid #1a2740;border-radius:8px;padding:12px;margin:4px 0;'>
              <div style='font-size:0.72rem;color:#4a6080;text-transform:uppercase;letter-spacing:0.1em;'>{k}</div>
              <div style='font-family:IBM Plex Mono,monospace;font-size:1.1rem;font-weight:600;color:{color};'>{v}</div>
            </div>
            """, unsafe_allow_html=True)

    badge = f"<span class='badge-ok'>✔ ESTABLE (Fo={Fo:.4f} ≤ 0.5)</span>" if estable else \
            f"<span class='badge-err'>✖ INESTABLE (Fo={Fo:.4f} > 0.5) — reducir DT_SEG o aumentar N_NODOS. DT_SEG máx: {int(0.5*RHO_AGUA*CP_AGUA*H_NODO**2/K_AGUA)} s</span>"
    st.markdown(f"**Estabilidad numérica (Fourier):** {badge}", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# EJECUCIÓN
# ─────────────────────────────────────────────────────────────────────────────
if ejecutar or "resultados" in st.session_state:

    if ejecutar:
        with st.spinner("⏳ Ejecutando simulación…"):
            caudal_kg_s, etiquetas_evento = construir_caudal_vector(
                EVENTOS_CONSUMO, N_PASOS, DT_SEG, RHO_AGUA
            )
            vol_diario_L = np.sum(caudal_kg_s) * DT_SEG / RHO_AGUA * 1000.0

            (T_hist, Q_calef_v, Q_perd_v,
             E_calef_kWh, E_perd_kWh,
             estado_calef, E_consumo_kWh, delta_E_alm) = simular_termotanque(
                n_nodos=N_NODOS, n_pasos=N_PASOS, dt_seg=DT_SEG,
                T_ini=T_INICIAL, T_amb=T_AMBIENTE, T_red=T_RED,
                M_nodo=M_NODO, Cp=CP_AGUA, Rho=RHO_AGUA,
                U_cond=U_COND, U_conv=U_CONV,
                A_lat=A_LAT_TANQ_NODO, A_tub=A_LAT_TUBO_NODO, A_tapa=A_TAPA,
                K_eff=K_EFF_NODOS, V_NODO_M3=V_NODO_M3,
                P_calef1=P_CALEFACTOR_1, P_calef2=P_CALEFACTOR_2,
                nodo_c1=NODO_CALEF_1, nodo_c2=NODO_CALEF_2,
                T_set=T_SETPOINT, T_dead=T_DEADBAND, nodo_sensor=NODO_SENSOR,
                C_inv=C_INVERSION, caudal_kg_s=caudal_kg_s
            )

        st.session_state["resultados"] = {
            "T_hist": T_hist, "Q_calef_v": Q_calef_v, "Q_perd_v": Q_perd_v,
            "E_calef_kWh": E_calef_kWh, "E_perd_kWh": E_perd_kWh,
            "estado_calef": estado_calef, "E_consumo_kWh": E_consumo_kWh,
            "delta_E_alm": delta_E_alm, "caudal_kg_s": caudal_kg_s,
            "vol_diario_L": vol_diario_L,
            # guardar config para mostrar
            "N_NODOS": N_NODOS, "H_NODO": H_NODO, "t_vec": t_vec,
            "T_SETPOINT": T_SETPOINT, "T_DEADBAND": T_DEADBAND,
            "T_RED": T_RED, "T_AMBIENTE": T_AMBIENTE, "T_INICIAL": T_INICIAL,
            "V_TOTAL_L": V_TOTAL_L, "P_CALEFACTOR": P_CALEFACTOR,
            "DURACION_HORAS": DURACION_HORAS, "DT_SEG": DT_SEG,
            "RHO_AGUA": RHO_AGUA, "EVENTOS_CONSUMO": EVENTOS_CONSUMO,
        }

    # Cargar resultados
    r = st.session_state["resultados"]
    T_hist       = r["T_hist"]
    Q_calef_v    = r["Q_calef_v"]
    Q_perd_v     = r["Q_perd_v"]
    E_calef_kWh  = r["E_calef_kWh"]
    E_perd_kWh   = r["E_perd_kWh"]
    estado_calef = r["estado_calef"]
    E_consumo_kWh= r["E_consumo_kWh"]
    delta_E_alm  = r["delta_E_alm"]
    caudal_kg_s  = r["caudal_kg_s"]
    vol_diario_L = r["vol_diario_L"]
    _N   = r["N_NODOS"]
    _HN  = r["H_NODO"]
    _tv  = r["t_vec"]
    _TS  = r["T_SETPOINT"]
    _TD  = r["T_DEADBAND"]
    _TR  = r["T_RED"]
    _TA  = r["T_AMBIENTE"]
    _TI  = r["T_INICIAL"]
    _VL  = r["V_TOTAL_L"]
    _PC  = r["P_CALEFACTOR"]
    _DH  = r["DURACION_HORAS"]
    _DT  = r["DT_SEG"]
    _RH  = r["RHO_AGUA"]
    _EV  = r["EVENTOS_CONSUMO"]

    T_media = T_hist.mean(axis=1)
    T_tope  = T_hist[:, _N - 1]
    T_fondo = T_hist[:, 0]

    eta_global       = (E_calef_kWh - E_perd_kWh) / max(E_calef_kWh, 1e-6) * 100
    balance_error    = E_calef_kWh - delta_E_alm - E_perd_kWh - E_consumo_kWh
    balance_relativo = abs(balance_error) / max(E_calef_kWh, 1e-6) * 100

    # ─────────────────────────────────────────────────────────────────────
    # TARJETAS DE MÉTRICAS
    # ─────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Resumen de Resultados</div>", unsafe_allow_html=True)
    mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
    metricas = [
        (mc1, f"{E_calef_kWh:.3f}", "kWh", "Energía calefactor"),
        (mc2, f"{E_perd_kWh:.3f}", "kWh", "Pérdidas térmicas"),
        (mc3, f"{delta_E_alm:.3f}", "kWh", "ΔE almacenada"),
        (mc4, f"{E_consumo_kWh:.3f}", "kWh", "E. al usuario"),
        (mc5, f"{eta_global:.1f}", "%",   "Eficiencia global"),
        (mc6, f"{vol_diario_L:.1f}", "L/día", "Volumen consumido"),
    ]
    for col, val, unit, label in metricas:
        col.markdown(f"""
        <div class='metric-card'>
          <span class='metric-value'>{val}</span>
          <span class='metric-unit'>{unit}</span>
          <div class='metric-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

    # Balance y estado
    st.markdown("")
    ba_col, bb_col = st.columns([1, 1])
    with ba_col:
        badge_bal = f"<span class='badge-ok'>✔ Error {balance_relativo:.3f} % (< 1 %)</span>" \
                    if balance_relativo < 1.0 else \
                    f"<span class='badge-err'>✖ Error {balance_relativo:.3f} % — revisar DT_SEG</span>"
        badge_eta = f"<span class='badge-warn'>⚠ η > 100% (absorbe calor del ambiente)</span>" \
                    if eta_global > 100 else \
                    f"<span class='badge-ok'>✔ η = {eta_global:.1f} %</span>"
        st.markdown(f"""
        <div class='results-section'>
          <h4>Balance Energético</h4>
          <div class='balance-row'><span class='balance-key'>E_calef</span><span class='balance-value'>{E_calef_kWh:.4f} kWh</span></div>
          <div class='balance-row'><span class='balance-key'>ΔE_alm</span><span class='balance-value'>{delta_E_alm:.4f} kWh</span></div>
          <div class='balance-row'><span class='balance-key'>E_perd</span><span class='balance-value'>{E_perd_kWh:.4f} kWh</span></div>
          <div class='balance-row'><span class='balance-key'>E_usuario</span><span class='balance-value'>{E_consumo_kWh:.4f} kWh</span></div>
          <div class='balance-row'><span class='balance-key'>Error absoluto</span><span class='balance-value'>{balance_error:+.5f} kWh</span></div>
          <div style='margin-top:10px;'>{badge_bal}</div>
          <div style='margin-top:6px;'>{badge_eta}</div>
        </div>
        """, unsafe_allow_html=True)
    with bb_col:
        st.markdown(f"""
        <div class='results-section'>
          <h4>Temperaturas Finales</h4>
          <div class='balance-row'><span class='balance-key'>T media tanque</span><span class='balance-value'>{T_media[-1]:.2f} °C</span></div>
          <div class='balance-row'><span class='balance-key'>T tope (nodo {_N-1})</span><span class='balance-value'>{T_tope[-1]:.2f} °C</span></div>
          <div class='balance-row'><span class='balance-key'>T fondo (nodo 0)</span><span class='balance-value'>{T_fondo[-1]:.2f} °C</span></div>
          <div class='balance-row'><span class='balance-key'>Gradiente tope–fondo</span><span class='balance-value'>{T_tope[-1]-T_fondo[-1]:.2f} °C</span></div>
          <div class='balance-row'><span class='balance-key'>Nodo sensor (termostato)</span><span class='balance-value'>Nodo {NODO_SENSOR}</span></div>
          <div class='balance-row'><span class='balance-key'>Fourier Fo</span>
            <span class='balance-value'>
              {Fo:.5f} {"<span class='badge-ok'>OK</span>" if Fo<=0.5 else "<span class='badge-err'>INESTABLE</span>"}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # TABS DE GRÁFICOS
    # ─────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Visualizaciones</div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Evolución Temporal",
        "🌡 Estratificación",
        "⚡ Análisis Energético",
        "🚿 Perfil de Consumo",
    ])

    # ── TAB 1: Evolución temporal ──────────────────────────────────────────
    with tab1:
        fig, axes = plt.subplots(3, 1, figsize=(14, 11), sharex=True)
        fig.patch.set_facecolor("#0d1520")
        fig.suptitle(
            f"Termotanque {_VL:.0f} L  ·  {_N} nodos  ·  {_DH} h simulación\n"
            f"T_amb={_TA}°C  |  Setpoint={_TS}°C  |  P_calef={_PC:.0f} W",
            fontsize=11, fontweight="bold", color="#c0cce0", y=0.99
        )

        cmap = plt.cm.plasma
        ax = axes[0]
        for i in range(_N):
            frac  = i / (_N - 1)
            color = cmap(frac)
            label = f"Nodo {i} ({(i+0.5)*_HN*100:.0f} cm)"
            ax.plot(_tv, T_hist[:, i], color=color, lw=1.1, alpha=0.88,
                    label=label if (i % 2 == 0 or i == _N-1) else "_nolegend_")
        ax.axhline(_TS, color="#ff4444", ls="--", lw=1.0, label=f"Setpoint {_TS}°C")
        ax.axhline(_TS - _TD, color="#ff9800", ls=":", lw=1.0,
                   label=f"Setpoint−banda ({_TS-_TD}°C)")
        for (hora_ini, dur_min, _, desc) in _EV:
            ax.axvspan(hora_ini, hora_ini + dur_min/60, alpha=0.1, color="cyan", lw=0)
        ax.set_ylabel("Temperatura [°C]")
        ax.set_title("Temperatura por nodo (0=fondo, N-1=tope)", fontsize=10)
        ax.legend(loc="upper right", fontsize=7, ncol=2, facecolor="#0d1520", edgecolor="#1e2d4a", labelcolor="#8a9bb5")

        ax2 = axes[1]
        ax2.fill_between(_tv, Q_calef_v/1000, color="#ff6b35", alpha=0.75, label="Potencia calef. [kW]", step="pre")
        ax2.fill_between(_tv, Q_perd_v/1000,  color="#4a8db5", alpha=0.55, label="Pérdidas [kW]",       step="pre")
        ax2_t = ax2.twinx()
        caudal_lmin = caudal_kg_s / _RH * 1000 * 60
        ax2_t.fill_between(_tv, caudal_lmin, color="#26c6da", alpha=0.35, label="Caudal [L/min]", step="pre")
        ax2_t.set_ylabel("Caudal [L/min]", color="#26c6da", fontsize=9)
        ax2_t.tick_params(axis="y", labelcolor="#26c6da")
        ax2_t.spines["right"].set_color("#1e3050")
        ax2.set_ylabel("Potencia [kW]")
        ax2.set_title("Potencia calefactor, pérdidas y caudal de consumo", fontsize=10)
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_t.get_legend_handles_labels()
        ax2.legend(lines1+lines2, labels1+labels2, loc="upper right", fontsize=8,
                   facecolor="#0d1520", edgecolor="#1e2d4a", labelcolor="#8a9bb5")

        ax3 = axes[2]
        ax3.plot(_tv, T_tope,  color="#ef5350", lw=1.8, label="Tope (nodo superior)")
        ax3.plot(_tv, T_media, color="#ff9800", lw=1.8, label="T media tanque", ls="--")
        ax3.plot(_tv, T_fondo, color="#42a5f5", lw=1.8, label="Fondo (nodo inferior)")
        ax3.axhline(_TS, color="#ff4444", ls="--", lw=0.8, alpha=0.5)
        ax3.set_xlabel("Hora [h]")
        ax3.set_ylabel("Temperatura [°C]")
        ax3.set_title("Temperaturas representativas del tanque", fontsize=10)
        ax3.legend(loc="lower right", fontsize=9, facecolor="#0d1520", edgecolor="#1e2d4a", labelcolor="#8a9bb5")
        ax3.set_xlim(0, _DH)
        ax3.xaxis.set_major_locator(mticker.MultipleLocator(2))
        for (hora_ini, _, _, _desc) in _EV:
            ax3.axvline(hora_ini, color="#26c6da", lw=0.7, ls=":", alpha=0.7)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── TAB 2: Estratificación ─────────────────────────────────────────────
    with tab2:
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.patch.set_facecolor("#0d1520")

        ax = axes[0]
        im = ax.pcolormesh(
            _tv,
            np.arange(_N) * _HN * 100,
            T_hist.T,
            cmap="inferno", shading="auto",
            vmin=_TR - 2, vmax=_TS + 2
        )
        cb = plt.colorbar(im, ax=ax, label="Temperatura [°C]")
        cb.ax.yaxis.set_tick_params(color="#8a9bb5")
        cb.outline.set_edgecolor("#1e2d4a")
        for lbl in cb.ax.yaxis.get_ticklabels():
            lbl.set_color("#8a9bb5")
        ax.set_xlabel("Hora del día [h]")
        ax.set_ylabel("Altura en el tanque [cm]")
        ax.set_title("Mapa de estratificación térmica\n(color = temperatura)", fontsize=10)
        for (hora_ini, dur_min, _, _desc) in _EV:
            ax.axvline(hora_ini, color="#00e5ff", lw=0.8, ls="--", alpha=0.8)

        ax2 = axes[1]
        horas_clave = sorted(set([_DH*0.05, _DH*0.1, _DH*0.3, _DH*0.6]))
        horas_clave = [h for h in horas_clave if h < _DH]
        colores_k   = ["#4fc3f7", "#29b6f6", "#ef5350", "#b71c1c"]
        alturas_cm  = (np.arange(_N) + 0.5) * _HN * 100
        for hora, color in zip(horas_clave[:4], colores_k):
            paso = min(int(hora * 3600 / _DT), len(T_hist)-1)
            ax2.plot(T_hist[paso, :], alturas_cm, "o-", color=color, lw=2,
                     markersize=5, label=f"{hora:.1f} h")
        ax2.axvline(_TS, color="#ff4444", ls="--", lw=1, label=f"Setpoint {_TS}°C")
        ax2.axvline(_TR, color="#26c6da", ls=":",  lw=1, label=f"T_red {_TR}°C")
        ax2.set_xlabel("Temperatura [°C]")
        ax2.set_ylabel("Altura en el tanque [cm]")
        ax2.set_title("Perfil vertical de temperatura\nen instantes seleccionados", fontsize=10)
        ax2.legend(fontsize=9, facecolor="#0d1520", edgecolor="#1e2d4a", labelcolor="#8a9bb5")
        ax2.set_ylim(0, H_TANQUE * 100)
        ax2.set_xlim(_TR - 3, _TS + 15)

        fig.suptitle(f"Estratificación Térmica · {_VL:.0f} L / {_N} nodos", fontsize=12, fontweight="bold", color="#c0cce0")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── TAB 3: Análisis energético ─────────────────────────────────────────
    with tab3:
        fig, axes = plt.subplots(1, 3, figsize=(17, 5))
        fig.patch.set_facecolor("#0d1520")
        fig.suptitle("Análisis Energético del Termotanque", fontsize=12, fontweight="bold", color="#c0cce0")

        E_calef_acum = np.cumsum(Q_calef_v) * _DT / 3_600_000.0
        E_perd_acum  = np.cumsum(Q_perd_v)  * _DT / 3_600_000.0

        ax = axes[0]
        ax.plot(_tv, E_calef_acum, color="#ef5350", lw=2, label="E. calefactor [kWh]")
        ax.plot(_tv, E_perd_acum,  color="#42a5f5", lw=2, label="Pérdidas acum. [kWh]")
        ax.fill_between(_tv, E_calef_acum, E_perd_acum, alpha=0.18, color="#4caf50", label="Energía útil neta")
        ax.set_xlabel("Hora [h]")
        ax.set_ylabel("Energía [kWh]")
        ax.set_title("Energía acumulada", fontsize=10)
        ax.legend(fontsize=8, facecolor="#0d1520", edgecolor="#1e2d4a", labelcolor="#8a9bb5")

        ax2 = axes[1]
        E_util = max(E_calef_kWh - E_perd_kWh, 0)
        sizes  = [E_util, E_perd_kWh] if E_util + E_perd_kWh > 0 else [1, 0]
        labels = [f"Energía útil\n({E_util:.3f} kWh)", f"Pérdidas\n({E_perd_kWh:.3f} kWh)"]
        colors_pie = ["#4caf50", "#ef5350"]
        wedges, texts, autotexts = ax2.pie(
            sizes, labels=labels, autopct="%1.1f%%",
            colors=colors_pie, startangle=90,
            wedgeprops=dict(edgecolor="#0d1520", linewidth=2),
            textprops={"color": "#8a9bb5", "fontsize": 9}
        )
        for at in autotexts: at.set_color("#0f1117"); at.set_fontweight("bold")
        ax2.set_title(f"Distribución energética\n(Total: {E_calef_kWh:.3f} kWh)", fontsize=10)

        ax3 = axes[2]
        ax3.plot(_tv, T_media, color="#ff9800", lw=2, label="T media tanque")
        on_total = (estado_calef[:, 0] + estado_calef[:, 1]).astype(float)
        ax3_t = ax3.twinx()
        ax3_t.fill_between(_tv, on_total, color="#ef5350", alpha=0.28, step="pre", label="Calefactores ON (0–2)")
        ax3_t.set_ylim(-0.5, 3); ax3_t.set_yticks([0, 1, 2])
        ax3_t.set_ylabel("N° calef. ON", color="#ef5350", fontsize=9)
        ax3_t.tick_params(axis="y", labelcolor="#ef5350")
        ax3_t.spines["right"].set_color("#1e3050")
        ax3.set_xlabel("Hora [h]"); ax3.set_ylabel("Temperatura [°C]")
        ax3.set_title("T media vs estado calefactor", fontsize=10)
        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_t.get_legend_handles_labels()
        ax3.legend(lines1+lines2, labels1+labels2, loc="lower right", fontsize=8,
                   facecolor="#0d1520", edgecolor="#1e2d4a", labelcolor="#8a9bb5")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── TAB 4: Perfil de consumo ───────────────────────────────────────────
    with tab4:
        if not _EV:
            st.info("No hay eventos de consumo definidos. Seleccione un perfil en la barra lateral o use 'Personalizado'.")
        else:
            fig, ax = plt.subplots(figsize=(14, 4))
            fig.patch.set_facecolor("#0d1520")
            colores_ev = plt.cm.tab20(np.linspace(0, 1, len(_EV)))
            for j, (hora, dur, caud, desc) in enumerate(_EV):
                ax.barh(y=0, width=dur/60, left=hora, height=0.6,
                        color=colores_ev[j], edgecolor="#0d1520", linewidth=1.5,
                        label=f"{desc} ({caud} L/min, {dur} min)")
                ax.text(hora + dur/120, 0, f"{caud}\nL/m", ha="center", va="center",
                        fontsize=7, color="white", fontweight="bold")

            ax.set_xlim(0, 24)
            ax.set_xlabel("Hora del día [h]")
            ax.set_title(
                f"Perfil de Consumo de Agua Caliente  ·  Total: {vol_diario_L:.1f} L/día",
                fontsize=11, fontweight="bold"
            )
            ax.set_yticks([])
            ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
            ax.legend(loc="upper right", fontsize=7, ncol=2, title="Eventos",
                      facecolor="#0d1520", edgecolor="#1e2d4a", labelcolor="#8a9bb5",
                      title_fontsize=7)
            for (x0, x1, label, color) in [
                (0, 6, "Noche", "#0a1520"), (6, 12, "Mañana", "#0d1a10"),
                (12, 18, "Tarde", "#0d0a1a"), (18, 24, "Noche", "#0a1520")
            ]:
                ax.axvspan(x0, x1, alpha=0.25, color=color, zorder=0)
                ax.text((x0+x1)/2, 0.38, label, ha="center", fontsize=8,
                        color="#3a5060", style="italic")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    # ─────────────────────────────────────────────────────────────────────
    # TABLA DE DATOS
    # ─────────────────────────────────────────────────────────────────────
    with st.expander("📋 Tabla de datos (submuestreo cada 15 min)", expanded=False):
        paso_15min = max(1, int(15 * 60 / _DT))
        idx_sub    = np.arange(0, len(T_hist), paso_15min)
        t_sub      = _tv[idx_sub]
        T_sub      = T_hist[idx_sub, :]
        Q_c_sub    = Q_calef_v[idx_sub]
        Q_p_sub    = Q_perd_v[idx_sub]
        caudal_sub = caudal_kg_s[idx_sub] / _RH * 1000 * 60

        df_data = {"Hora [h]": np.round(t_sub, 3)}
        df_data["T_media [°C]"] = np.round(T_sub.mean(axis=1), 2)
        df_data["T_tope [°C]"]  = np.round(T_sub[:, -1], 2)
        df_data["T_fondo [°C]"] = np.round(T_sub[:, 0], 2)
        df_data["Q_calef [W]"]  = np.round(Q_c_sub, 1)
        df_data["Q_pérd [W]"]   = np.round(Q_p_sub, 1)
        df_data["Caudal [L/min]"] = np.round(caudal_sub, 3)
        for i in range(_N):
            df_data[f"Nodo {i} [°C]"] = np.round(T_sub[:, i], 2)

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, height=350)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Descargar CSV",
            data=csv,
            file_name="termotanque_simulacion.csv",
            mime="text/csv"
        )

else:
    # Estado inicial — sin simulación ejecutada
    st.markdown("""
    <div style='background:#0d1520;border:1px solid #1a2740;border-radius:12px;padding:40px;text-align:center;margin:20px 0;'>
      <div style='font-size:3rem;margin-bottom:16px;'>🌡</div>
      <div style='font-family:IBM Plex Mono,monospace;font-size:1.1rem;font-weight:600;color:#4a7ab5;margin-bottom:8px;'>
        SIMULACIÓN NO EJECUTADA
      </div>
      <div style='color:#3a5060;font-size:0.9rem;'>
        Configure los parámetros en la barra lateral y presione <strong style='color:#ff8c42;'>▶ EJECUTAR SIMULACIÓN</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar descripción del modelo
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
        <div class='results-section'>
          <h4>Modelo Matemático</h4>
          <div style='font-size:0.85rem;color:#6a8aaa;line-height:1.7;'>
            Balance de energía por nodo:<br>
            <code style='color:#ff8c42;'>M·Cp·dT/dt = Q̇_calef − Q̇_pérd + Q̇_cond + Q̇_advec + Q̇_inv</code><br><br>
            Integración Euler explícito · Criterio de Fourier Fo ≤ 0.5<br>
            Mezcla por inversión de densidad (InversionMixing)
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_d2:
        st.markdown("""
        <div class='results-section'>
          <h4>Referencias</h4>
          <div style='font-size:0.85rem;color:#6a8aaa;line-height:1.7;'>
            · EnergyPlus Engineering Reference v26.1.0<br>
            &nbsp;&nbsp;§19.3.3 Stratified Water Thermal Tank<br>
            · ASHRAE Standard 90.1<br>
            · ISO 9459-2 (calentadores solares)
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-top:40px;padding:16px;border-top:1px solid #1a2740;text-align:center;
            font-family:IBM Plex Mono,monospace;font-size:0.72rem;color:#2a3a50;'>
  Termotanque · Estratificación Térmica · Modelo EnergyPlus WaterHeater:Stratified ·
  Python 3 · Streamlit · numpy / matplotlib
</div>
""", unsafe_allow_html=True)
