import streamlit as st
import pandas as pd
import math

# --- FUNCIÓN DE CÁLCULO PROFESIONAL (POISSON) ---
def poisson_over(lam, line):
    """Calcula la probabilidad de que ocurran MÁS eventos que 'line' dado un promedio 'lam'"""
    # Probabilidad de que ocurran exactamente k eventos: (lambda^k * e^-lambda) / k!
    # Para el "Más de", calculamos 1 - (suma de probabilidades de 0 a floor(line))
    prob_under = sum([(math.exp(-lam) * (lam**i)) / math.factorial(i) for i in range(int(line) + 1)])
    return round((1 - prob_under) * 100, 1)

st.set_page_config(page_title="Analizador Pro - Tablas", layout="wide")
st.title("📊 Botanalist Pro: Análisis de Probabilidades")

# Inputs de usuario (Aquí pondrás los promedios obtenidos de tu API)
col1, col2 = st.columns(2)
# Valores por defecto para pruebas
local_goles = col1.number_input("Media Goles Local", 1.5, step=0.1)
visita_goles = col2.number_input("Media Goles Visita", 1.2, step=0.1)

local_corners = col1.number_input("Media Corners Local", 5.0, step=0.1)
visita_corners = col2.number_input("Media Corners Visita", 4.5, step=0.1)

if st.button("Generar Tablas de Probabilidad"):
    
    # --- TABLA DE GOLES ---
    st.subheader("⚽ Análisis de Goles")
    lines = [2.5, 3.5, 4.5, 5.5]
    data_goles = []
    for l in lines:
        data_goles.append({
            "Línea": f"Más de {l}",
            "Local (%)": poisson_over(local_goles, l),
            "Visita (%)": poisson_over(visita_goles, l),
            "Media (%)": poisson_over((local_goles + visita_goles)/2, l)
        })
    st.table(pd.DataFrame(data_goles))

    # --- TABLA DE CORNERS ---
    st.subheader("🚩 Análisis de Córners")
    c_lines = [6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
    data_corners = []
    for l in c_lines:
        data_corners.append({
            "Línea": f"Más de {l}",
            "Local (%)": poisson_over(local_corners, l),
            "Visita (%)": poisson_over(visita_corners, l),
            "Media (%)": poisson_over((local_corners + visita_corners)/2, l)
        })
    st.table(pd.DataFrame(data_corners))

    st.success("Análisis generado con distribución de Poisson acumulada.")
