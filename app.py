import streamlit as st
import math

# --- FUNCIÓN DE DATOS (AQUÍ ES DONDE ALIMENTAS LA APP) ---
def get_team_stats(team_name):
    # En el futuro, aquí conectarás a la API real. 
    # Por ahora, estos son los datos que la app procesará.
    return {
        "goles": 2.1, 
        "corners": 5.4, 
        "tiros_arco": 6.2, 
        "tarjetas": 1.8
    }

st.set_page_config(page_title="Analizador Pro", layout="wide")
st.title("⚽ Dashboard de Análisis Predictivo")

col1, col2 = st.columns(2)
local = col1.text_input("Equipo Local", "Real Madrid")
visita = col2.text_input("Equipo Visitante", "Barcelona")

if st.button("Analizar Partido"):
    with st.spinner("Calculando probabilidades..."):
        data_l = get_team_stats(local)
        data_v = get_team_stats(visita)
        
        # --- CÁLCULOS AUTOMÁTICOS ---
        stats = ["goles", "corners", "tiros_arco", "tarjetas"]
        
        st.subheader("Análisis Comparativo (Promedios)")
        
        for stat in stats:
            val_l = data_l[stat]
            val_v = data_v[stat]
            total = val_l + val_v
            
            # Cálculo de probabilidad simple
            prob_l = (val_l / total) * 100 if total > 0 else 50
            
            # Visualización profesional
            st.write(f"**{stat.upper()}**")
            c1, c2, c3 = st.columns([1, 1, 2])
            c1.metric(local, val_l)
            c2.metric(visita, val_v)
            c3.progress(prob_l / 100)
            st.write(f"Probabilidad de dominio en {stat}: {local} {prob_l:.1f}% vs {visita} {100-prob_l:.1f}%")
            st.divider()

        # --- MODELO DE POISSON (Para Goles) ---
        st.subheader("Modelo Predictivo: Probabilidad de Goles (Poisson)")
        def poisson_prob(lmbda, k):
            return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)
        
        # Probabilidad de victoria según Poisson (Simplificado)
        win_prob = (data_l['goles'] / (data_l['goles'] + data_v['goles'])) * 100
        st.success(f"Probabilidad de victoria estimada para {local}: {win_prob:.2f}%")
