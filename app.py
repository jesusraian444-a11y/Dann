import streamlit as st
import requests
import math


# --- CONFIGURACIÓN ---
# En Streamlit Cloud, ve a "Settings" -> "Secrets" y agrega:
# API_KEY = * b4dde78817a19a675c2f692dad2dc05a
API_KEY = st.secrets.get("b4dde78817a19a675c2f692dad2dc05a")

def get_team_stats(team_name):
    """Función simulada para llamar a la API"""
    # Aquí iría la lógica real de request.get(...)
    # Por ahora, es un esquema para que veas dónde va la magia
    # url = f"https://api-football.com/v3/teams?search={team_name}"
    # headers = {'x-rapidapi-key': API_KEY}
    # response = requests.get(url, headers=headers)
    # return response.json()
    return {"goles": 2.1, "corners": 5.4, "tiros": 12.0} # Datos de prueba

def poisson_prob(lmbda, k):
    """Cálculo de probabilidad de Poisson: P(X=k) = (lambda^k * e^-lambda) / k!"""
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

st.title("⚽ Analizador Pro: Data Science Edition")

# --- UI ---
local = st.text_input("Equipo Local")
visita = st.text_input("Equipo Visitante")

if st.button("Analizar Partido"):
    with st.spinner("Conectando a la base de datos..."):
        # 1. Integración de datos (Simulada)
        stats_local = get_team_stats(local)
        stats_visita = get_team_stats(visita)
        
        # 2. Análisis Estadístico
        st.subheader("Estadísticas Recopiladas")
        col1, col2 = st.columns(2)
        col1.metric("Goles Esperados (L)", stats_local['goles'])
        col2.metric("Goles Esperados (V)", stats_visita['goles'])
        
        # 3. Modelo de Probabilidad (Poisson)
        st.subheader("Modelo Predictivo (Poisson)")
        
        # Probabilidad de que el local gane
        # Comparativa simplificada de lambda
        prob_local_win = (stats_local['goles'] / (stats_local['goles'] + stats_visita['goles'])) * 100
        
        st.write(f"Probabilidad de victoria para {local}: {prob_local_win:.2f}%")
        st.progress(prob_local_win / 100)
        
        st.write(f"Probabilidad de victoria para {visita}: {100 - prob_local_win:.2f}%")
        st.progress((100 - prob_local_win) / 100)
        
        # Análisis de riesgo
        if abs(prob_local_win - 50) < 5:
            st.warning("Partido equilibrado: Riesgo alto.")
        elif prob_local_win > 60:
            st.success(f"Alta confianza en victoria de {local}")

    
