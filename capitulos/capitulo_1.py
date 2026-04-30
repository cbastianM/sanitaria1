"""
Capítulo 1: Fundamentos de Ingeniería Sanitaria
Conceptos básicos, dotaciones, caudales de diseño
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def render():
    """Función principal que renderiza el capítulo"""
    
    st.markdown("<h1 class='chapter-header'>1️⃣ Fundamentos de Sanitaria</h1>", unsafe_allow_html=True)
    
    # Menú de secciones dentro del capítulo
    seccion = st.tabs([
        "📖 Teoría",
        "🧮 Calculadora de Caudales",
        "📊 Gráficos",
        "✏️ Ejercicios"
    ])
    
    # === SECCIÓN 1: TEORÍA ===
    with seccion[0]:
        teoria_fundamentos()
    
    # === SECCIÓN 2: CALCULADORA ===
    with seccion[1]:
        calculadora_caudales()
    
    # === SECCIÓN 3: GRÁFICOS ===
    with seccion[2]:
        graficos_variacion()
    
    # === SECCIÓN 4: EJERCICIOS ===
    with seccion[3]:
        ejercicios_practicos()


def teoria_fundamentos():
    """Contenido teórico del capítulo"""
    
    st.markdown("""
    ## Conceptos Fundamentales
    
    ### ¿Qué es la Ingeniería Sanitaria?
    
    La ingeniería sanitaria es la rama de la ingeniería civil que se encarga de:
    - **Abastecimiento** de agua potable a las comunidades
    - **Tratamiento** del agua para hacerla apta para el consumo
    - **Recolección y tratamiento** de aguas residuales
    - **Disposición** segura de residuos
    
    ### Variables Clave en Diseño
    
    #### 1. Dotación (d)
    Cantidad de agua que se asigna a cada habitante por día.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Dotación Urbana", "120-150", "L/hab/día")
    with col2:
        st.metric("Dotación Rural", "50-100", "L/hab/día")
    with col3:
        st.metric("Comercial/Industrial", "20-50", "L/hab/día (adicional)")
    
    st.markdown("""
    ---
    
    #### 2. Población de Diseño
    
    Se calcula proyectando la población actual hacia el futuro (generalmente 25-30 años).
    
    **Métodos comunes:**
    - Aritmético: P = P₀ + K·t
    - Geométrico: P = P₀(1 + r)ᵗ
    - Exponencial: P = P₀·eʳᵗ
    
    ---
    
    #### 3. Caudales Característicos (RAS 2017)
    
    | Símbolo | Descripción | Fórmula |
    |---------|-------------|---------|
    | **Qmd** | Caudal medio diario | Qmd = P·d / 86400 |
    | **QMD** | Caudal máximo diario | QMD = Qmd · K₁ |
    | **QMH** | Caudal máximo horario | QMH = Qmd · K₁ · K₂ |
    
    Donde:
    - **K₁** = Factor de variación diaria (1.2 - 1.5)
    - **K₂** = Factor de variación horaria (1.4 - 2.0)
    - **P** = Población (habitantes)
    - **d** = Dotación (L/hab/día)
    
    ---
    
    ### Ejemplo de Cálculo
    
    Para una población de 10,000 habitantes con dotación de 130 L/hab/día:
    """)
    
    # Ejemplo interactivo
    col1, col2, col3 = st.columns(3)
    with col1:
        poblacion = 10000
        st.write(f"**Población:** {poblacion:,} hab")
    with col2:
        dotacion = 130
        st.write(f"**Dotación:** {dotacion} L/hab/día")
    with col3:
        k1, k2 = 1.3, 1.6
        st.write(f"**K₁:** {k1}, **K₂:** {k2}")
    
    qmd = (poblacion * dotacion) / 86400
    qmd_m3_s = qmd / 1000
    qmd_m3_h = qmd_m3_s * 3600
    
    QMD = qmd * k1
    QMH = qmd * k1 * k2
    
    st.markdown(f"""
    **Cálculos:**
    - Qmd = (10,000 hab × 130 L/hab/día) / 86,400 s/día = **{qmd:.2f} L/s** ({qmd_m3_h:.2f} m³/h)
    - QMD = {qmd:.2f} L/s × {k1} = **{QMD:.2f} L/s**
    - QMH = {qmd:.2f} L/s × {k1} × {k2} = **{QMH:.2f} L/s**
    """)


def calculadora_caudales():
    """Calculadora interactiva de caudales"""
    
    st.markdown("## 🧮 Calculadora de Caudales")
    
    # Inputs en columnas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        poblacion = st.number_input(
            "Población (habitantes)",
            min_value=100,
            max_value=1000000,
            value=50000,
            step=1000
        )
    
    with col2:
        dotacion = st.number_input(
            "Dotación (L/hab/día)",
            min_value=20,
            max_value=300,
            value=130,
            step=5
        )
    
    with col3:
        st.markdown("**Factores de variación**")
    
    col1, col2 = st.columns(2)
    with col1:
        k1 = st.slider("K₁ (Factor diario)", 1.1, 1.5, 1.3, 0.1)
    with col2:
        k2 = st.slider("K₂ (Factor horario)", 1.4, 2.5, 1.6, 0.1)
    
    # Cálculos
    qmd = (poblacion * dotacion) / 86400  # L/s
    qmd_m3_h = (qmd / 1000) * 3600
    QMD = qmd * k1  # L/s
    QMH = qmd * k1 * k2  # L/s
    
    # Resultados en tarjetas
    st.markdown("---")
    st.markdown("### Resultados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Qmd (L/s)",
            f"{qmd:.2f}",
            f"{qmd_m3_h:.2f} m³/h"
        )
    
    with col2:
        st.metric(
            "QMD (L/s)",
            f"{QMD:.2f}",
            f"{QMD/1000*3600:.2f} m³/h"
        )
    
    with col3:
        st.metric(
            "QMH (L/s)",
            f"{QMH:.2f}",
            f"{QMH/1000*3600:.2f} m³/h"
        )
    
    with col4:
        st.metric(
            "Volumen diario",
            f"{(qmd/1000*86400):.0f}",
            "m³/día"
        )
    
    # Tabla de resumen
    st.markdown("---")
    st.markdown("### Tabla de Resumen")
    
    datos = {
        "Parámetro": ["Qmd", "QMD", "QMH"],
        "L/s": [f"{qmd:.2f}", f"{QMD:.2f}", f"{QMH:.2f}"],
        "m³/h": [f"{qmd_m3_h:.2f}", f"{QMD/1000*3600:.2f}", f"{QMH/1000*3600:.2f}"],
        "m³/día": [f"{qmd/1000*86400:.2f}", f"{QMD/1000*86400:.2f}", f"{QMH/1000*86400:.2f}"]
    }
    
    df = pd.DataFrame(datos)
    st.dataframe(df, use_container_width=True)


def graficos_variacion():
    """Gráficos de variación de caudales"""
    
    st.markdown("## 📊 Variación de Caudales en el Tiempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        poblacion = st.number_input(
            "Población",
            min_value=1000,
            max_value=500000,
            value=50000,
            key="pop_grafico"
        )
    
    with col2:
        dotacion = st.number_input(
            "Dotación (L/hab/día)",
            min_value=50,
            max_value=200,
            value=130,
            key="dot_grafico"
        )
    
    # Variación a lo largo del día
    horas = np.arange(0, 24, 0.5)
    qmd = (poblacion * dotacion) / 86400
    k1 = 1.3
    k2 = 1.6
    
    # Simulación de caudal a lo largo del día (patrón típico)
    # Mayor en la mañana y noche, menor en la madrugada
    patron = 0.5 + 0.3 * np.sin((horas - 6) * np.pi / 12) + 0.3 * np.sin((horas - 20) * np.pi / 8)
    patron = np.maximum(patron, 0.3)  # Mínimo 30% del promedio
    
    caudales = qmd * patron
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=horas,
        y=caudales,
        mode='lines+markers',
        name='Caudal horario',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_hline(y=qmd, line_dash="dash", line_color="green", 
                  name=f"Qmd ({qmd:.2f} L/s)")
    fig.add_hline(y=qmd*k1, line_dash="dash", line_color="orange", 
                  name=f"QMD ({qmd*k1:.2f} L/s)")
    fig.add_hline(y=qmd*k1*k2, line_dash="dash", line_color="red", 
                  name=f"QMH ({qmd*k1*k2:.2f} L/s)")
    
    fig.update_layout(
        title="Variación de Caudal a lo largo del día",
        xaxis_title="Hora del día",
        yaxis_title="Caudal (L/s)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de crecimiento poblacional
    st.markdown("---")
    st.markdown("### Crecimiento Poblacional Proyectado")
    
    años_proyeccion = st.slider("Años de proyección", 5, 50, 25, 5)
    
    años = np.arange(0, años_proyeccion + 1)
    tasa_crecimiento = 0.025  # 2.5% anual
    
    poblacion_proyectada = poblacion * (1 + tasa_crecimiento) ** años
    qmd_proyectado = (poblacion_proyectada * dotacion) / 86400
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=años,
        y=poblacion_proyectada,
        mode='lines+markers',
        name='Población',
        yaxis='y1',
        line=dict(color='#2ca02c', width=2)
    ))
    
    fig2.add_trace(go.Scatter(
        x=años,
        y=qmd_proyectado,
        mode='lines+markers',
        name='Qmd',
        yaxis='y2',
        line=dict(color='#d62728', width=2)
    ))
    
    fig2.update_layout(
        title=f"Proyección a {años_proyeccion} años",
        xaxis_title="Año",
        yaxis=dict(title="Población (hab)", side='left'),
        yaxis2=dict(title="Qmd (L/s)", overlaying='y', side='right'),
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True)


def ejercicios_practicos():
    """Sección de ejercicios"""
    
    st.markdown("## ✏️ Ejercicios Prácticos")
    
    # Ejercicio 1
    with st.expander("**Ejercicio 1:** Cálculo de caudales básicos", expanded=True):
        st.markdown("""
        Un municipio tiene una población actual de 25,000 habitantes. Se requiere diseñar
        el sistema de abastecimiento de agua para los próximos 25 años considerando
        una tasa de crecimiento del 2% anual y una dotación de 120 L/hab/día.
        
        Calcular: Qmd, QMD y QMH para el año 25 (K₁=1.3, K₂=1.6)
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Datos:**")
            st.write("- Población actual: 25,000 hab")
            st.write("- Tasa crecimiento: 2% anual")
            st.write("- Proyección: 25 años")
            st.write("- Dotación: 120 L/hab/día")
        
        with col2:
            if st.checkbox("Ver solución 1"):
                # Cálculo
                p0 = 25000
                r = 0.02
                t = 25
                d = 120
                k1, k2 = 1.3, 1.6
                
                p25 = p0 * (1 + r) ** t
                qmd = (p25 * d) / 86400
                QMD = qmd * k1
                QMH = qmd * k1 * k2
                
                st.success(f"""
                **Solución:**
                - P₂₅ = 25,000 × (1.02)²⁵ = {p25:,.0f} hab
                - Qmd = {qmd:.2f} L/s
                - QMD = {QMD:.2f} L/s
                - QMH = {QMH:.2f} L/s
                """)
    
    # Ejercicio 2
    with st.expander("**Ejercicio 2:** Volumen de tanque de almacenamiento"):
        st.markdown("""
        Con los datos del ejercicio anterior, calcular el volumen del tanque
        de almacenamiento asumiendo que debe garantizar 8 horas de suministro
        con el QMD.
        """)
        
        if st.checkbox("Ver solución 2"):
            qmd_ej2 = 8.78  # Del ejercicio anterior
            QMD_ej2 = qmd_ej2 * 1.3
            tiempo_horas = 8
            
            volumen_m3 = (QMD_ej2 / 1000) * 3600 * tiempo_horas
            volumen_litros = volumen_m3 * 1000
            
            st.success(f"""
            **Solución:**
            - V = QMD × tiempo × 3600
            - V = ({QMD_ej2:.2f} L/s) × 8 h × 3600 s/h
            - V = {volumen_m3:.2f} m³ = {volumen_litros:,.0f} L
            """)