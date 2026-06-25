import streamlit as st
import pandas as pd
import math

# --- FUNCIÓN DE CÁLCULO DE PROBABILIDAD (POISSON) ---
def poisson_over(lam, line):
    """Calcula la probabilidad de que ocurran MÁS eventos que 'line' basado en la media 'lam'"""
    if lam <= 0: return 0
    prob_under = sum([(math.exp(-lam) * (lam**i)) / math.factorial(i) for i in range(int(line) + 1)])
    return round((1 - prob_under) * 100, 1)

# --- BASE DE DATOS SIMULADA ---
def get_stats(team_name):
    # Aquí puedes añadir más equipos cuando tengas la API real
    db = {
        "real madrid": {"goles": 2.5, "corners": 6.5, "tiros": 15.0},
        "barcelona": {"goles": 2.3, "corners": 6.0, "tiros": 14.0},
        "manchester city": {"goles": 2.8, "corners": 7.5, "tiros": 17.0},
        "default": {"goles": 1.5, "corners": 5.0, "tiros": 10.0}
    }
    # Convertimos a minúsculas para que no importe si escriben en mayúsculas
    return db.get(team_name.lower(), db["default"])

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Analizador Pro", layout="wide")
st.title("⚽ Botanalist Pro: Análisis Predictivo")

# --- SELECCIÓN DE EQUIPOS ---
col1, col2 = st.columns(2)
local = col1.text_input("Equipo Local", "Real Madrid")
visita = col2.text_input("Equipo Visitante", "Barcelona")

if st.button("Analizar Partido"):
    with st.spinner("Procesando datos y calculando probabilidades..."):
        # Obtener datos
        data_l = get_stats(local)
        data_v = get_stats(visita)
        
        # --- TABLAS DE ANÁLISIS ---
        categorias = [
            ("⚽ Goles", "goles", [2.5, 3.5, 4.5]),
            ("🚩 Córners", "corners", [6.5, 7.5, 8.5, 9.5]),
            ("🎯 Tiros al Arco", "tiros", [8.5, 10.5, 12.5])
        ]
        
        for titulo, key, lineas in categorias:
            st.subheader(titulo)
            data_tabla = []
            for l in lineas:
                data_tabla.append({
                    "Línea": f"Más de {l}",
                    f"{local} (%)": poisson_over(data_l[key], l),
                    f"{visita} (%)": poisson_over(data_v[key], l),
                    "Media (%)": poisson_over((data_l[key] + data_v[key])/2, l)
                })
            
            # Mostrar tabla profesional
            st.table(pd.DataFrame(data_tabla))
            st.divider()

    st.success("Análisis completado con éxito.")
