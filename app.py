import streamlit as st
import math
import random

# --- BASE DE DATOS SIMULADA (MOCK) ---
# Aquí simulamos que el sistema "conoce" a los equipos
def get_team_stats(team_name):
    # Esto es una base de datos ficticia. Cuando tengas la API real, 
    # aquí es donde harás la consulta para reemplazar estos números fijos.
    db = {
        "real madrid": {"goles": 2.5, "corners": 6.2, "tiros": 15.0, "tarjetas": 1.5},
        "barcelona": {"goles": 2.3, "corners": 5.8, "tiros": 14.2, "tarjetas": 1.7},
        "manchester city": {"goles": 2.7, "corners": 7.0, "tiros": 16.5, "tarjetas": 1.2},
        "default": {"goles": 1.5, "corners": 4.5, "tiros": 10.0, "tarjetas": 2.0}
    }
    # Buscamos el equipo en minúsculas
    return db.get(team_name.lower(), db["default"])

st.set_page_config(page_title="Analizador Pro", layout="wide")
st.title("⚽ Dashboard de Análisis Predictivo Realista")

col1, col2 = st.columns(2)
local = col1.text_input("Equipo Local")
visita = col2.text_input("Equipo Visitante")

if st.button("Analizar Partido"):
    if local and visita:
        with st.spinner("Analizando disparidad de fuerzas..."):
            # Obtener datos de la "DB"
            data_l = get_team_stats(local)
            data_v = get_team_stats(visita)
            
            # --- FACTOR LOCAL ---
            # En la vida real, el local tiene un plus (normalmente +0.2 goles)
            data_l['goles'] += 0.2 
            
            st.subheader(f"📊 Análisis: {local} vs {visita}")
            
            # Comparativa de métricas
            stats = ["goles", "corners", "tiros", "tarjetas"]
            
            for stat in stats:
                val_l = data_l[stat]
                val_v = data_v[stat]
                
                # Cálculo de probabilidad con "fuerza relativa"
                # Usamos una fórmula de ponderación profesional
                total_fuerza = val_l + val_v
                prob_l = (val_l / total_fuerza) * 100
                
                st.write(f"**{stat.upper()}**")
                c1, c2, c3 = st.columns([1, 1, 3])
                c1.metric(local, f"{val_l:.1f}")
                c2.metric(visita, f"{val_v:.1f}")
                
                # Barra dinámica
                c3.progress(prob_l / 100)
                st.caption(f"Tendencia: {local} {prob_l:.1f}% | {visita} {100-prob_l:.1f}%")
                st.divider()

            # --- MODELO PREDICTIVO ---
            st.subheader("🎯 Predicción Final")
            # Diferencia de goles como indicador de victoria
            diff = data_l['goles'] - data_v['goles']
            if diff > 0.5:
                resultado = f"Alta probabilidad de victoria para {local}"
            elif diff < -0.5:
                resultado = f"Alta probabilidad de victoria para {visita}"
            else:
                resultado = "Partido equilibrado: Posible empate"
            
            st.success(resultado)
    else:
        st.warning("Por favor ingresa ambos equipos para comenzar.")
