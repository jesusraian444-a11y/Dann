import streamlit as st

st.title("⚽ Mi Analizador de Fútbol")

# Pestañas para organizar
tab1, tab2 = st.tabs(["Ingreso de Datos", "Análisis"])

with tab1:
    st.header("Datos del Partido")
    col1, col2 = st.columns(2)
    local = col1.text_input("Equipo Local")
    visita = col2.text_input("Equipo Visitante")
    
    st.write("---")
    st.subheader("Estadísticas:")
    corners_local = st.number_input("Corners Equipo Local", 0)
    corners_visita = st.number_input("Corners Equipo Visitante", 0)
    
    tarjetas_local = st.number_input("Tarjetas Equipo Local", 0)
    tarjetas_visita = st.number_input("Tarjetas Equipo Visitante", 0)
    
    goles_local = st.number_input("Goles Promedio Local", 0.0, step=0.1)
    goles_visita = st.number_input("Goles Promedio Visita", 0.0, step=0.1)

with tab2:
    if st.button("Generar Predicción"):
        if local and visita:
            st.success(f"Analizando: {local} vs {visita}")
            
            # Cálculos
            total_corners = corners_local + corners_visita
            total_tarjetas = tarjetas_local + tarjetas_visita
            total_goles = goles_local + goles_visita
            
            # Cálculo de probabilidades basado en goles
            if total_goles > 0:
                prob_local = (goles_local / total_goles) * 100
                prob_visita = (goles_visita / total_goles) * 100
            else:
                prob_local, prob_visita = 50, 50

            # Resultados Numéricos
            st.subheader("Estadísticas Totales")
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Total Corners", total_corners)
            col_m2.metric("Total Tarjetas", total_tarjetas)
            col_m3.metric("Total Goles", f"{total_goles:.1f}")
            
            st.write("---")
            
            # Gráficos de probabilidad
            st.subheader("Probabilidad de Victoria")
            st.write(f"**{local}:** {prob_local:.1f}%")
            st.progress(prob_local / 100)
            
            st.write(f"**{visita}:** {prob_visita:.1f}%")
            st.progress(prob_visita / 100)
            
            # Predicción final
            if prob_local > prob_visita:
                st.write(f"🏆 **Ganador probable:** {local}")
            elif prob_visita > prob_local:
                st.write(f"🏆 **Ganador probable:** {visita}")
            else:
                st.write("🤝 **Pronóstico:** Empate técnico probable")
        else:
            st.error("Por favor, ingresa los nombres de los equipos.")

