import streamlit as st
import pandas as pd
import math

# --- LÓGICA MATEMÁTICA ---
def poisson_over(lam, line):
    # Cálculo de probabilidad usando solo librerías estándar
    prob_under = sum([(math.pow(lam, i) * math.exp(-lam)) / math.factorial(i) for i in range(int(line) + 1)])
    return round((1 - prob_under) * 100, 1)

# --- BASE DE DATOS ---
def get_stats(team_name):
    # Estadísticas base. Puedes editar estos números para ajustar tus predicciones
    db = {
        "real madrid": {"goles": 2.5, "corners": 6.8, "tiros": 16.0, "tarjetas": 2.2},
        "tunez": {"goles": 0.9, "corners": 3.2, "tiros": 8.0, "tarjetas": 3.5},
        "países bajos": {"goles": 2.0, "corners": 6.0, "tiros": 14.0, "tarjetas": 1.8},
        "manchester city": {"goles": 2.8, "corners": 7.5, "tiros": 18.0, "tarjetas": 1.5}
    }
    return db.get(team_name.lower(), {"goles": 1.5, "corners": 5.0, "tiros": 10.0, "tarjetas": 2.0})

# --- ESTILO PROFESIONAL (HEATMAP) ---
def color_conditional(val):
    try:
        # Convertimos "45.0%" a número 45.0
        num = float(str(val).replace('%', ''))
        # Colores estilo apuestas
        if num >= 70: color = '#a9dfbf' # Verde claro
        elif num >= 50: color = '#f9e79f' # Amarillo
        else: color = '#f5b7b1' # Rojo claro
        return f'background-color: {color}; color: black'
    except:
        return ''

# --- INTERFAZ ---
st.set_page_config(page_title="Botanalist Pro", layout="wide")
st.title("⚽ Botanalist: Motor de Pronósticos")

col1, col2 = st.columns(2)
local = col1.text_input("Equipo Local", "Real Madrid")
visita = col2.text_input("Equipo Visitante", "Tunez")

if st.button("Generar Pronóstico Profesional"):
    stats_l = get_stats(local)
    stats_v = get_stats(visita)
    
    mercados = {
        "⚽ GOLES": {"stat": "goles", "lines": [1.5, 2.5, 3.5, 4.5]},
        "🚩 CÓRNERS": {"stat": "corners", "lines": [7.5, 9.5, 11.5]},
        "🎯 TIROS AL ARCO": {"stat": "tiros", "lines": [8.5, 10.5, 12.5]},
        "🟨 TARJETAS": {"stat": "tarjetas", "lines": [1.5, 2.5, 3.5]}
    }
    
    for titulo, cfg in mercados.items():
        st.subheader(titulo)
        
        datos = []
        for l in cfg["lines"]:
            p_l = poisson_over(stats_l[cfg["stat"]], l)
            p_v = poisson_over(stats_v[cfg["stat"]], l)
            media = round((p_l + p_v) / 2, 1)
            
            datos.append({
                "Línea": f"Más de {l}",
                f"{local.capitalize()}": f"{p_l}%",
                f"{visita.capitalize()}": f"{p_v}%",
                "Media (%)": f"{media}%"
            })
        
        # Crear DataFrame
        df = pd.DataFrame(datos)
        
        # APLICAR ESTILO (Cambiado a .map para compatibilidad moderna)
        styled_df = df.style.map(
            color_conditional, 
            subset=[f"{local.capitalize()}", f"{visita.capitalize()}", "Media (%)"]
        )
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        st.divider()

st.success("Pronóstico generado con formato profesional.")
