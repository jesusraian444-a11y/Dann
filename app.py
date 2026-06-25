import streamlit as st

st.title("⚽ Mi Analizador de Fútbol")

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
            
            total_corners = corners_local + corners_visita
            total_tarjetas = tarjetas_local + tarjetas_visita
            total_goles = goles_local + goles_visita
            
            st.metric("Corners Totales Probables", total_corners)
            st.metric("Tarjetas Totales Probables", total_tarjetas)
            st.metric("Goles Totales Esperados", f"{total_goles:.1f}")
            
            if goles_local > goles_visita:
                st.write(f"🏆 **Ganador probable:** {local}")
            elif goles_visita > goles_local:
                st.write(f"🏆 **Ganador probable:** {visita}")
            else:
                st.write("🤝 **Pronóstico:** Empate probable")
        else:
            st.error("Por favor, pon el nombre de los equipos primero.")
