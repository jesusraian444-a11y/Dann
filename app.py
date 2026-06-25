import streamlit as st
import pandas as pd
import math

# --- LÓGICA DE PROBABILIDAD ---
def get_poisson_over(lam, k):
    """Calcula la probabilidad de que ocurran MÁS eventos que 'k'."""
    prob_under = sum([(math.pow(lam, i) * math.exp(-lam)) / math.factorial(i) for i in range(int(k) + 1)])
    return round((1 - prob_under) * 100, 1)

# --- ESTILO ---
def apply_color(val):
    try:
        num = float(str(val).replace('%', ''))
        if num > 60: return 'background-color: #a9dfbf; color: black'
        elif num > 40: return 'background-color: #f9e79f; color: black'
        else: return 'background-color: #f5b7b1; color: black'
    except: return ''

# --- INTERFAZ ---
st.set_page_config(page_title="Predictor Mundial", layout="wide")
st.title("⚽ Predictor: Estadísticas Reales (Últimos 14 partidos)")

# --- ENTRADA DE DATOS ---
with st.expander("📊 Ingresa los totales de los últimos 14 partidos"):
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Equipo Local")
        l_goles = st.number_input("Total Goles (14 partidos)", 0, 100, 20)
        l_corners = st.number_input("Total Corners", 0, 200, 80)
        l_tiros = st.number_input("Total Tiros al arco", 0, 200, 100)
        l_tarjetas = st.number_input("Total Tarjetas", 0, 50, 20)
        
    with col_b:
        st.subheader("Equipo Visitante")
        v_goles = st.number_input("Total Goles (14 partidos) ", 0, 100, 15)
        v_corners = st.number_input("Total Corners ", 0, 200, 70)
        v_tiros = st.number_input("Total Tiros al arco ", 0, 200, 90)
        v_tarjetas = st.number_input("Total Tarjetas ", 0, 50, 25)

if st.button("Calcular Probabilidades Reales"):
    # Calculamos la media (Lambda) dividiendo entre 14
    stats_l = {"goles": l_goles/14, "corners": l_corners/14, "tiros": l_tiros/14, "tarjetas": l_tarjetas/14}
    stats_v = {"goles": v_goles/14, "corners": v_corners/14, "tiros": v_tiros/14, "tarjetas": v_tarjetas/14}
    
    mercados = {
        "⚽ GOLES": {"stat": "goles", "lines": [0.5, 1.5, 2.5, 3.5]},
        "🚩 CÓRNERS": {"stat": "corners", "lines": [6.5, 8.5, 10.5]},
        "🎯 TIROS": {"stat": "tiros", "lines": [8.5, 10.5, 12.5]},
        "🟨 TARJETAS": {"stat": "tarjetas", "lines": [1.5, 2.5, 3.5]}
    }

    for titulo, cfg in mercados.items():
        st.subheader(titulo)
        datos = []
        for l in cfg["lines"]:
            p_local = get_poisson_over(stats_l[cfg["stat"]], l)
            p_visita = get_poisson_over(stats_v[cfg["stat"]], l)
            datos.append({
                "Línea": f"Más de {l}",
                "Prob. Local": f"{p_local}%",
                "Prob. Visitante": f"{p_visita}%",
                "Promedio": f"{round((p_local + p_visita)/2, 1)}%"
            })
        
        df = pd.DataFrame(datos)
        styled_df = df.style.map(apply_color, subset=["Prob. Local", "Prob. Visitante", "Promedio"])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        st.divider()
