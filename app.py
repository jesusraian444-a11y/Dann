import streamlit as st
import pandas as pd
import math

# --- MOTOR DE CÁLCULO (POISSON) ---
def get_poisson_over(lam, k):
    """Calcula la probabilidad de que ocurran MÁS eventos que 'k'."""
    if lam <= 0: return 0.0 # Evitar errores si no hay datos
    prob_under = sum([(math.pow(lam, i) * math.exp(-lam)) / math.factorial(i) for i in range(int(k) + 1)])
    return round((1 - prob_under) * 100, 1)

# --- ESTILO HEATMAP (COLORES) ---
def apply_color(val):
    try:
        num = float(str(val).replace('%', ''))
        if num >= 70: return 'background-color: #a9dfbf; color: black' # Verde
        elif num >= 45: return 'background-color: #f9e79f; color: black' # Amarillo
        else: return 'background-color: #f5b7b1; color: black' # Rojo
    except: return ''

# --- INTERFAZ ---
st.set_page_config(page_title="Analizador Mundial", layout="wide")
st.title("⚽ Predictor Profesional: Últimos 20 Partidos")

# Entrada de nombres
col_names1, col_names2 = st.columns(2)
nombre_local = col_names1.text_input("Nombre Equipo Local", "Ej: Argentina")
nombre_visita = col_names2.text_input("Nombre Equipo Visitante", "Ej: Francia")

# Entrada de datos estadísticos
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader(f"📊 {nombre_local if nombre_local else 'Local'}")
    l_g = st.number_input(f"Goles en últimos 20 partidos ({nombre_local})", 0, 100, 30)
    l_c = st.number_input(f"Córners en últimos 20 partidos ({nombre_local})", 0, 300, 120)
    l_t = st.number_input(f"Tiros al arco en últimos 20 partidos ({nombre_local})", 0, 300, 100)
    l_tar = st.number_input(f"Tarjetas en últimos 20 partidos ({nombre_local})", 0, 100, 25)

with c2:
    st.subheader(f"📊 {nombre_visita if nombre_visita else 'Visitante'}")
    v_g = st.number_input(f"Goles en últimos 20 partidos ({nombre_visita})", 0, 100, 25)
    v_c = st.number_input(f"Córners en últimos 20 partidos ({nombre_visita})", 0, 300, 110)
    v_t = st.number_input(f"Tiros al arco en últimos 20 partidos ({nombre_visita})", 0, 300, 90)
    v_tar = st.number_input(f"Tarjetas en últimos 20 partidos ({nombre_visita})", 0, 100, 30)

st.markdown("---")

if st.button("🚀 Generar Pronóstico Real"):
    # Cálculo de medias (Lambda = Total / 20)
    stats_l = {"goles": l_g/20, "corners": l_c/20, "tiros": l_t/20, "tarjetas": l_tar/20}
    stats_v = {"goles": v_g/20, "corners": v_c/20, "tiros": v_t/20, "tarjetas": v_tar/20}
    
    mercados = {
        "⚽ GOLES": {"stat": "goles", "lines": [0.5, 1.5, 2.5, 3.5]},
        "🚩 CÓRNERS": {"stat": "corners", "lines": [7.5, 9.5, 11.5, 13.5]},
        "🎯 TIROS AL ARCO": {"stat": "tiros", "lines": [8.5, 10.5, 12.5, 14.5]},
        "🟨 TARJETAS": {"stat": "tarjetas", "lines": [1.5, 2.5, 3.5, 4.5]}
    }

    for titulo, cfg in mercados.items():
        st.subheader(titulo)
        datos = []
        for l in cfg["lines"]:
            p_local = get_poisson_over(stats_l[cfg["stat"]], l)
            p_visita = get_poisson_over(stats_v[cfg["stat"]], l)
            
            datos.append({
                "Línea": f"Más de {l}",
                f"{nombre_local} (%)": f"{p_local}%",
                f"{nombre_visita} (%)": f"{p_visita}%"
            })
        
        df = pd.DataFrame(datos)
        # Formato profesional con colores
        styled_df = df.style.map(
            apply_color, 
            subset=[f"{nombre_local} (%)", f"{nombre_visita} (%)"]
        )
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
