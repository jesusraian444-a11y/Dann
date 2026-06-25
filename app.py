import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# Configuración de página estilo profesional
st.set_page_config(page_title="Botanalist Pro - Betting Engine", layout="wide")
st.title("📊 Botanalist: Motor de Pronósticos Profesional")

# --- BASE DE DATOS REALISTA (Ajusta los valores aquí para cambiar el pronóstico) ---
def get_team_data(name):
    # Valores de Ataque (Goles esperados)
    db = {
        "real madrid": {"goles": 2.2, "corners": 6.5, "tiros": 15.0, "tarjetas": 1.5},
        "barcelona": {"goles": 2.0, "corners": 6.0, "tiros": 14.0, "tarjetas": 1.8},
        "getafe": {"goles": 0.8, "corners": 3.5, "tiros": 8.0, "tarjetas": 3.2},
        "celta vigo": {"goles": 1.1, "corners": 4.0, "tiros": 9.5, "tarjetas": 2.5}
    }
    return db.get(name.lower(), {"goles": 1.5, "corners": 5.0, "tiros": 11.0, "tarjetas": 2.0})

# --- MOTOR DE CÁLCULO (Poisson Match Probability) ---
def calc_match_prob(avg_local, avg_visit, line):
    # Combinamos la fuerza de ambos equipos para el evento
    lambda_match = avg_local + avg_visit
    # Poisson acumulada para obtener la probabilidad de Over
    prob_over = 1 - poisson.cdf(line, lambda_match)
    return round(prob_over * 100, 1)

# --- INTERFAZ ---
col1, col2 = st.columns(2)
team_local = col1.text_input("Equipo Local", "Real Madrid")
team_visit = col2.text_input("Equipo Visitante", "Getafe")

if st.button("Generar Pronóstico Real"):
    stats_l = get_team_data(team_local)
    stats_v = get_team_data(team_visit)

    st.subheader(f"Análisis: {team_local} vs {team_visit}")
    
    # Definición de Mercados
    mercados = {
        "⚽ GOLES": {"stat": "goles", "lines": [1.5, 2.5, 3.5, 4.5]},
        "🚩 CÓRNERS": {"stat": "corners", "lines": [7.5, 8.5, 9.5, 10.5]},
        "🎯 TIROS AL ARCO": {"stat": "tiros", "lines": [8.5, 10.5, 12.5, 14.5]},
        "🟨 TARJETAS": {"stat": "tarjetas", "lines": [1.5, 2.5, 3.5, 4.5]}
    }

    for titulo, cfg in mercados.items():
        st.write(f"### {titulo}")
        
        # Generar tabla con cálculos únicos
        data = []
        for l in cfg["lines"]:
            # Aquí está la clave: el cálculo se hace combinando ambos equipos
            prob = calc_match_prob(stats_l[cfg["stat"]], stats_v[cfg["stat"]], l)
            data.append({
                "Línea": f"Más de {l}",
                "Probabilidad (%)": prob,
                "Estado": "Alta" if prob > 60 else ("Media" if prob > 40 else "Baja")
            })
        
        df = pd.DataFrame(data)
        
        # Estilo profesional tipo tabla de apuestas
        st.dataframe(df, column_config={
            "Probabilidad (%)": st.column_config.ProgressColumn(
                "Probabilidad", format="%f%%", min_value=0, max_value=100
            )
        }, hide_index=True, use_container_width=True)
