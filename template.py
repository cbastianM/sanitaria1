"""
TEMPLATE - Capítulo [NÚMERO]: [NOMBRE]

Descripción del contenido que irá en este capítulo
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render():
    """Función principal que renderiza el capítulo"""
    
    st.markdown("<h1 class='chapter-header'>[ICONO] [NÚMERO]. [NOMBRE DEL CAPÍTULO]</h1>", unsafe_allow_html=True)
    
    # Menú de secciones dentro del capítulo
    seccion = st.tabs([
        "📖 Teoría",
        "🧮 Herramientas",
        "📊 Gráficos",
        "✏️ Ejercicios"
    ])
    
    # === SECCIÓN 1: TEORÍA ===
    with seccion[0]:
        teoria()
    
    # === SECCIÓN 2: HERRAMIENTAS ===
    with seccion[1]:
        herramientas()
    
    # === SECCIÓN 3: GRÁFICOS ===
    with seccion[2]:
        graficos()
    
    # === SECCIÓN 4: EJERCICIOS ===
    with seccion[3]:
        ejercicios()


def teoria():
    """Contenido teórico del capítulo"""
    
    st.markdown("""
    ## Título de la sección
    
    Aquí va el contenido teórico...
    
    ### Concepto 1
    Descripción...
    
    ### Concepto 2
    Descripción...
    """)


def herramientas():
    """Calculadoras y herramientas interactivas"""
    
    st.markdown("## Herramientas Interactivas")
    
    # Ejemplo de inputs
    col1, col2 = st.columns(2)
    
    with col1:
        valor1 = st.number_input("Parámetro 1", value=100)
    
    with col2:
        valor2 = st.number_input("Parámetro 2", value=50)
    
    # Cálculos
    resultado = valor1 + valor2
    
    st.metric("Resultado", f"{resultado}")


def graficos():
    """Gráficos y visualizaciones"""
    
    st.markdown("## Visualizaciones")
    
    # Ejemplo de gráfico simple
    datos = {
        'x': np.linspace(0, 10, 100),
        'y': np.sin(np.linspace(0, 10, 100))
    }
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=datos['x'], y=datos['y'], mode='lines'))
    fig.update_layout(title="Ejemplo de gráfico")
    
    st.plotly_chart(fig, use_container_width=True)


def ejercicios():
    """Ejercicios prácticos"""
    
    st.markdown("## Ejercicios Prácticos")
    
    with st.expander("**Ejercicio 1:** Descripción"):
        st.markdown("""
        Enunciado del problema...
        """)
        
        if st.checkbox("Ver solución"):
            st.success("**Solución:** ...")