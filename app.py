import streamlit as st
import pandas as pd
import math

# --- LÓGICA DE PROBABILIDAD POISSON (Sin librerías externas) ---
def poisson_over(mu, k):
    """Calcula la probabilidad de que ocurran > k eventos dado un promedio mu."""
    # Probabilidad acumulada (Under)
    prob_under = sum([(math.pow(mu, i) * math.exp(-mu)) / math.factorial(i) for i in range(int(k) + 1)])
    # Probabilidad de Over
    prob_over = 1 - prob_under
    return round(prob_over * 100, 1)

# --- BASE DE DATOS (AQUÍ PONES LOS DATOS DEL MUNDIAL) ---
# Edita estos valores con las estadísticas reales de tus partidos
def get_stats(team_name):
    db = {
        "tunez": {"goles": 0.8, "corners": 3.5, "tiros": 7.0, "tarjetas": 2.1},
        "paises bajos": {"goles": 1.9, "corners": 6.2, "tiros": 14.5, "tarjetas": 1.2},
        "real madrid": {"goles": 2.4, "corners": 6.8, "tiros": 15.5, "tarjetas": 1.5},
        "barcelona": {"goles": 2.2, "corners": 6.1, "tiros": 14.2, "tarjetas": 1.8}
    }
    # Si el equipo no está, usa un promedio estándar
    return db.get(team_name.lower(), {"goles": 1.2, "corners": 4.5, "tiros": 9.0, "tarjetas": 1.8})

# --- INTERFAZ ---
st.set_page_config(page_title="Botanalist Pro", layout="wide")
st.title("⚽ Botanalist: Motor de Pronósticos")

# Entradas
c1, c2 = st.columns(2)
local = c1.text_input("Equipo Local", "Tunez")
visita = c2.text_input("Equipo Visitante", "Paises Bajos")

if st.button("Analizar"):
    # Obtener stats
    stats_l = get_stats(local)
    stats_v = get_stats(visita)
    
    mercados = {
        "GOLES": {"key": "goles", "lines": [0.5, 1.5, 2.5]},
        "CÓRNERS": {"key": "corners", "lines": [7.5, 9.5, 11.5]},
        "TIROS": {"key": "tiros", "lines": [8.5, 10.5, 12.5]},
        "TARJETAS": {"key": "tarjetas", "lines": [1.5, 2.5, 3.5]}
    }
    
    for titulo, cfg in mercados.items():
        st.subheader(titulo)
        
        datos = []
        for l in cfg["lines"]:
            p_l = poisson_over(stats_l[cfg["key"]], l)
            p_v = poisson_over(stats_v[cfg["key"]], l)
            media = round((p_l + p_v) / 2, 1)
            
            datos.append({
                "Línea": f"Más de {l}",
                f"{local.capitalize()}": f"{p_l}%",
                f"{visita.capitalize()}": f"{p_v}%",
                "Media": f"{media}%"
            })
        
        st.table(pd.DataFrame(datos))
        st.divider()

st.info("Nota: Para obtener resultados distintos, asegúrate de que los equipos tengan promedios diferentes en la base de datos.")
