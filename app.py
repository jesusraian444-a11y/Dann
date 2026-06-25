import streamlit as st

st.title("⚽ Super Analizador Pro")

# Pestañas para organizar
tab1, tab2 = st.tabs(["Ingreso de Datos", "Análisis"])

with tab1:
    st.header("Datos del Partido")
    c1, c2 = st.columns(2)
    local = c1.text_input("Equipo Local")
    visita = c2.text_input("Equipo Visitante")
    
    st.write("---")
    st.subheader("Estadísticas:")
    
    # Usaremos 3 columnas para que quepa bien en el móvil
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.write("⚽ Goles")
        goles_local = st.number_input("Gol L", 0.0, step=0.1, key="gl")
        goles_visita = st.number_input("Gol V", 0.0, step=0.1, key="gv")
        
    with col_b:
        st.write("🚩 Corners")
        corn_l = st.number_input("Cor L", 0, key="cl")
        corn_v = st.number_input("Cor V", 0, key="cv")
        
    with col_c:
        st.write("🟨 Tarjetas")
        tarj_l = st.number_input("Tar L", 0, key="tl")
        tarj_v = st.number_input("Tar V", 0, key="tv")

    st.write("---")
    st.subheader("Estadísticas de Juego:")
    col_d, col_e, col_f = st.columns(3)
    
    with col_d:
        st.write("🚫 Faltas")
        faltas_l = st.number_input("Fal L", 0, key="fl")
        faltas_v = st.number_input("Fal V", 0, key="fv")
        
    with col_e:
        st.write("🎯 Tiros Totales")
        tiros_l = st.number_input("Tir L", 0, key="til")
        tiros_v = st.number_input("Tir V", 0, key="tiv")
        
    with col_f:
        st.write("🥅 Tiros Arco")
        arco_l = st.number_input("Arc L", 0, key="al")
        arco_v = st.number_input("Arc V", 0, key="av")

with tab2:
    if st.button("Generar Análisis Completo"):
        if local and visita:
            st.success(f"Analizando: {local} vs {visita}")
            
            # Cálculos
            tot_gol = goles_local + goles_visita
            tot_corn = corn_l + corn_v
            tot_tarj = tarj_l + tarj_v
            tot_faltas = faltas_l + faltas_v
            tot_tiros = tiros_l + tiros_v
            tot_arco = arco_l + arco_v
            
            # Resultados en métricas (2 filas)
            st.subheader("Resumen Total")
            m1, m2, m3 = st.columns(3)
            m1.metric("Goles", f"{tot_gol:.1f}")
            m2.metric("Corners", tot_corn)
            m3.metric("Tarjetas", tot_tarj)
            
            m4, m5, m6 = st.columns(3)
            m4.metric("Faltas", tot_faltas)
            m5.metric("Tiros", tot_tiros)
            m6.metric("Al Arco", tot_arco)
            
            # Probabilidades
            if tot_gol > 0:
                prob_l = (goles_local / tot_gol) * 100
                prob_v = (goles_visita / tot_gol) * 100
            else:
                prob_l, prob_v = 50, 50

            st.write("---")
            st.subheader("Probabilidad de Victoria")
            st.write(f"**{local}:** {prob_l:.1f}%")
            st.progress(prob_l / 100)
            st.write(f"**{visita}:** {prob_v:.1f}%")
            st.progress(prob_v / 100)
        else:
            st.error("Por favor, ingresa los nombres de los equipos.")

