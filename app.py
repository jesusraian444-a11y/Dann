import streamlit as st
import pandas as pd
import math

# --- FUNCIÓN MATEMÁTICA: DISTRIBUCIÓN POISSON ---
def poisson_prob_over(lam, line):
    """Calcula la probabilidad real de que ocurran MÁS de 'line' eventos."""
    # Probabilidad acumulada de 0 a floor(line)
    prob_under = sum([(math.exp(-lam) * (lam**i)) / math.factorial(i) for i in range(int(line) + 1)])
    # Probabilidad de Over = 1 - Probabilidad de Under
    return round((1 - prob_under) * 100, 1)

# --- BASE DE DATOS (AQUÍ ESTÁ LA MAGIA) ---
def get_team_stats(team_name):
    # Stats medias por partido. (Puedes editar estos números)
    db = {
        "real madrid": {"goles": 2.4, "corners": 6.2, "tiros": 14.5, "tarjetas": 1.9},
        "barcelona": {"goles": 2.1, "corners": 5.8, "tiros": 13.8, "tarjetas": 2.1},
        "manchester city": {"goles": 2.7, "corners": 7.0, "tiros": 16.2, "tarjetas": 1.4},
        "default": {"goles": 1.5, "corners": 5.0, "tiros": 10.0, "tarjetas": 1.8}
    }
    return db.get(team_name.lower(), db["default"])

# --- INTERFAZ ---
st.set_page_config(page_title="Analizador Pro", layout="wide")
st.title("📊 Pronosticador Profesional (Poisson Engine)")

col1, col2 = st.columns(2)
local = col1.text_input("Equipo Local", "Real Madrid")
visita = col2.text_input("Equipo Visitante", "Barcelona")

if st.button("Generar Probabilidades"):
    data_l = get_team_stats(local)
    data_v = get_team_stats(visita)

    # Definimos qué líneas queremos analizar por cada estadística
    config = {
        "⚽ GOLES": {"key": "goles", "lines": [1.5, 2.5, 3.5]},
        "🚩 CÓRNERS": {"key": "corners", "lines": [7.5, 8.5, 9.5, 10.5]},
        "🎯 TIROS AL ARCO": {"key": "tiros", "lines": [8.5, 10.5, 12.5]},
        "🟨 TARJETAS AMARILLAS": {"key": "tarjetas", "lines": [1.5, 2.5, 3.5]}
    }

    for titulo, cfg in config.items():
        st.subheader(titulo)
        
        table_data = []
        for l in cfg['lines']:
            table_data.append({
                "Línea": f"Más de {l}",
                f"{local} (%)": poisson_prob_over(data_l[cfg['key']], l),
                f"{visita} (%)": poisson_prob_over(data_v[cfg['key']], l)
            })
        
        df = pd.DataFrame(table_data)
        st.table(df)
        st.divider()

st.info("Nota: Los porcentajes se calculan mediante la distribución de Poisson, reflejando la probabilidad real de superar la línea establecida.")
