"""
Capítulo 2: Pérdidas por Fricción en Tuberías
Procedimiento iterativo: Reynolds → Swamme Jain → Darcy-Weisbach
Rugosidad absoluta K = 1×10⁻⁶ m (PVC)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# Constantes
K = 1e-6  # Rugosidad absoluta en metros (PVC)
G = 9.81  # Aceleración gravitatoria
NU = 1e-6  # Viscosidad cinemática (agua a 20°C) en m²/s

def render():
    """Función principal que renderiza el capítulo"""
    
    st.markdown("<h1 class='chapter-header'>Capitulo 2: Perdidas por Friccion en Tuberias</h1>", unsafe_allow_html=True)
    
    # Menu de secciones dentro del capitulo
    seccion = st.tabs([
        "Teoria y Formulas",
        "Calculadora Iterativa",
        "Graficos",
        "Ejercicios"
    ])
    
    # === SECCIÓN 1: TEORÍA ===
    with seccion[0]:
        teoria_formulas()
    
    # === SECCIÓN 2: CALCULADORA ===
    with seccion[1]:
        calculadora_perdidas()
    
    # === SECCIÓN 3: GRÁFICOS ===
    with seccion[2]:
        graficos_perdidas()
    
    # === SECCIÓN 4: EJERCICIOS ===
    with seccion[3]:
        ejercicios_practicos()


def teoria_formulas():
    """Contenido teórico organizado por pasos del procedimiento"""
    
    st.markdown("""
    ## Procedimiento de Calculo de Perdidas por Friccion
    
    El calculo sigue un **procedimiento iterativo** aplicando formulas fundamentales hasta convergencia.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Paso 1: Numero de Reynolds")
        st.latex(r"\mathrm{Re} = \frac{V \cdot D}{\nu}")
        st.markdown("**Donde:**")
        st.markdown("- **V**: Velocidad (m/s)")
        st.markdown("- **D**: Diametro (m)")
        st.markdown("- **nu**: Viscosidad cinematica")
        st.markdown("**Regimen:**")
        st.markdown("- Re < 2300: Laminar")
        st.markdown("- 2300-4000: Transitorio")
        st.markdown("- Re > 4000: Turbulento")
        
        st.markdown("### Paso 2: Swamme Jain")
        st.latex(r"f = \frac{1.325}{\left[\ln\left(\frac{5.74}{\mathrm{Re}^{0.9}} + \frac{K}{3.7D}\right)\right]^2}")
        st.markdown("**Donde:**")
        st.markdown("- **f**: Factor de friccion")
        st.markdown("- **K**: Rugosidad (m)")
        
    with col2:
        st.markdown("### Paso 3: Colebrook-White")
        st.latex(r"\frac{1}{\sqrt{f}} = -2 \log_{10}\left(\frac{k}{3.7D} + \frac{2.51}{\mathrm{Re}\sqrt{f}}\right)")
        st.markdown("**Donde:**")
        st.markdown("- **f**: Factor de friccion")
        st.markdown("- **k**: Rugosidad (m)")
        
        st.markdown("### Proceso Iterativo")
        st.markdown("""
        1. Calcular **f₀** con Swamme Jain
        2. Reemplazar **f₀** en el lado derecho de Colebrook-White:
        """)
        st.latex(r"\frac{1}{\sqrt{f_1}} = -2 \log_{10}\left(\frac{k}{3.7D} + \frac{2.51}{\mathrm{Re}\sqrt{f_0}}\right)")
        st.markdown("""
        3. Resolver el lado derecho y despejar **f₁** del lado izquierdo
        4. Verificar que **f₁** hace que la igualdad se cumpla:
           - Reemplazar **f₁** en ambos lados de Colebrook-White
           - Si ambos lados son iguales o muy parecidos, cumple
        """)
        
        st.markdown("### Paso 4: Darcy-Weisbach")
        st.latex(r"h_f = f \cdot \frac{L}{D} \cdot \frac{V^2}{2g}")
        st.markdown("**Donde:**")
        st.markdown("- **hf**: Perdidas (m)")
        st.markdown("- **L**: Longitud (m)")
        st.markdown("- **g**: 9.81 m/s^2")


def calculadora_perdidas():
    """Calculadora interactiva con procedimiento iterativo paso a paso"""
    
    st.markdown("## Calculadora Iterativa de Perdidas por Friccion")
    
    st.info("""
    **Instrucciones:**
    1. Ingresa el **Caudal (Q)** en L/s
    2. Ingresa el **Diametro de la tuberia** en mm
    3. Ingresa la **Longitud** de la conduccion en m
    4. La calculadora realizara el proceso iterativo automaticamente
    """)
    
    # INPUTS
    st.markdown("### Datos de Entrada")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        q_l_s = st.number_input(
            "Caudal (L/s)",
            min_value=0.1,
            max_value=500.0,
            value=50.0,
            step=1.0
        )
        q_m3_s = q_l_s / 1000  # Convertir a m³/s
    
    with col2:
        diametro_mm = st.number_input(
            "Diámetro (mm)",
            min_value=10,
            max_value=2000,
            value=150,
            step=10
        )
        diametro = diametro_mm / 1000  # Convertir a metros
    
    with col3:
        longitud = st.number_input(
            "Longitud (m)",
            min_value=10,
            max_value=50000,
            value=1000,
            step=100
        )
    
    # CÁLCULOS
    st.markdown("### Paso 1: Calculo de Velocidad y Reynolds")
    
    # Calcular velocidad
    area = np.pi * (diametro / 2) ** 2
    velocidad = q_m3_s / area
    
    # Calcular Reynolds
    reynolds = (velocidad * diametro) / NU
    
    # Determinar régimen
    if reynolds < 2300:
        regimen = "LAMINAR"
        color_regimen = "Laminar"
    elif reynolds < 4000:
        regimen = "TRANSITORIO"
        color_regimen = "Transitorio"
    else:
        regimen = "TURBULENTO"
        color_regimen = "Turbulento"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Velocidad (V)", f"{velocidad:.3f}", "m/s")
    with col2:
        st.metric("Reynolds (Re)", f"{reynolds:.0f}", "")
    with col3:
        st.metric("Régimen", regimen, color_regimen)
    with col4:
        st.metric("Viscosidad (ν)", f"{NU:.0e}", "m²/s")
    
    st.markdown("### Paso 2-5: Procedimiento Iterativo")
    
    # Función para calcular factor f usando Swamme Jain
    def swamme_jain(re, k, d):
        try:
            arg = (5.74 / (re ** 0.9)) + (k / (3.7 * d))
            f = 1.325 / (np.log(arg) ** 2)
            return f
        except:
            return 0.02
    
    # Función para calcular factor f usando Colebrook-White
    def colebrook_white(re, k, d, f_guess):
        try:
            # Procedimiento iterativo manual:
            # 1. Evaluar lado derecho con f_guess
            # 2. 1/√f_nuevo = lado_derecho
            # 3. Despejar f_nuevo
            term1 = k / (3.7 * d)
            term2 = 2.51 / (re * np.sqrt(f_guess))
            lado_derecho = -2 * np.log10(term1 + term2)
            f_new = (1 / lado_derecho) ** 2
            return f_new
        except:
            return f_guess
    
    # Iteración
    tolerancia = 0.0001
    max_iteraciones = 20
    f_actual = swamme_jain(reynolds, K, diametro)
    
    iteraciones_data = []
    
    for i in range(max_iteraciones):
        f_anterior = f_actual
        f_actual = colebrook_white(reynolds, K, diametro, f_anterior)
        
        iteraciones_data.append({
            "Iteración": i + 1,
            "f anterior": f"{f_anterior:.6f}",
            "f nuevo": f"{f_actual:.6f}",
            "Diferencia": f"{abs(f_actual - f_anterior):.6f}",
            "Converge": "SI" if abs(f_actual - f_anterior) < tolerancia else "NO"
        })
        
        if abs(f_actual - f_anterior) < tolerancia:
            break
    
    # Mostrar tabla de iteraciones
    df_iter = pd.DataFrame(iteraciones_data)
    st.dataframe(df_iter, use_container_width=True, hide_index=True)
    
    st.markdown("### Paso 6: Calculo de Perdidas con Darcy-Weisbach")
    
    # Calcular pérdidas
    hf = f_actual * (longitud / diametro) * (velocidad ** 2 / (2 * G))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Factor de Fricción (f)",
            f"{f_actual:.6f}",
            "final"
        )
    
    with col2:
        st.metric(
            "Pérdidas (hf)",
            f"{hf:.3f}",
            "metros"
        )
    
    # TABLA RESUMEN
    st.markdown("### Resumen Final de Calculos")
    
    resumen_data = {
        "Parámetro": [
            "Caudal (Q)",
            "Diámetro (D)",
            "Longitud (L)",
            "Velocidad (V)",
            "Reynolds (Re)",
            "Régimen",
            "Rugosidad (K)",
            "Factor de fricción (f)",
            "Pérdidas por fricción (hf)",
            "Pérdidas unitarias (hf/L)"
        ],
        "Valor": [
            f"{q_l_s:.2f} L/s",
            f"{diametro_mm} mm",
            f"{longitud} m",
            f"{velocidad:.4f} m/s",
            f"{reynolds:.0f}",
            regimen,
            f"{K:.0e} m",
            f"{f_actual:.6f}",
            f"{hf:.4f} m",
            f"{hf/longitud:.6f} m/m"
        ]
    }
    
    df_resumen = pd.DataFrame(resumen_data)
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)
    
    # Guardar en session state para gráficos
    st.session_state.q_l_s = q_l_s
    st.session_state.diametro = diametro
    st.session_state.longitud = longitud
    st.session_state.velocidad = velocidad
    st.session_state.reynolds = reynolds
    st.session_state.f = f_actual
    st.session_state.hf = hf
    st.session_state.regimen = regimen


def graficos_perdidas():
    """Gráficos de análisis de pérdidas"""
    
    st.markdown("## Visualizacion de Resultados")
    
    if not hasattr(st.session_state, 'hf'):
        st.warning("Primero debes usar la **Calculadora Iterativa** para generar los datos.")
        return
    
    # Gráfico: Cota Piezométrica
    st.markdown("### Cota Piezométrica")
    
    longitud = st.session_state.longitud
    hf_total = st.session_state.hf
    
    x = np.linspace(0, longitud, 100)
    
    # Línea de terreno en cero
    terreno = np.zeros_like(x)
    
    # Línea de energía en 100
    linea_energia = np.full_like(x, 100.0)
    
    # Línea piezométrica (100 - pérdidas acumuladas)
    perdidas_acum = (hf_total / longitud) * x
    piezometrica = 100.0 - perdidas_acum
    
    fig1 = go.Figure()
    
    # Terreno
    fig1.add_trace(go.Scatter(
        x=x,
        y=terreno,
        mode='lines',
        name='Terreno',
        line=dict(color='#8B4513', width=2),
        fill='tozeroy',
        fillcolor='rgba(139, 69, 19, 0.15)'
    ))
    
    # Línea de energía
    fig1.add_trace(go.Scatter(
        x=x,
        y=linea_energia,
        mode='lines',
        name='Línea de Energía',
        line=dict(color='#2ca02c', width=2, dash='dash')
    ))
    
    # Línea piezométrica
    fig1.add_trace(go.Scatter(
        x=x,
        y=piezometrica,
        mode='lines',
        name='Línea Piezométrica',
        line=dict(color='#1f77b4', width=3)
    ))
    
    # Punto inicial
    fig1.add_trace(go.Scatter(
        x=[0],
        y=[100.0],
        mode='markers',
        marker=dict(size=12, color='green'),
        name='Inicio',
        showlegend=False
    ))
    
    # Punto final
    fig1.add_trace(go.Scatter(
        x=[longitud],
        y=[100.0 - hf_total],
        mode='markers',
        marker=dict(size=12, color='red'),
        name='Final',
        showlegend=False
    ))
    
    fig1.update_layout(
        title="Perfil de Cota Piezométrica",
        xaxis_title="Distancia (m)",
        yaxis_title="Cota (m)",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        showlegend=True
    )
    
    st.plotly_chart(fig1, use_container_width=True)


def ejercicios_practicos():
    """Ejercicios prácticos con soluciones"""
    
    st.markdown("## Ejercicios Practicos")
    
    # Ejercicio 1
    with st.expander("**Ejercicio 1:** Cálculo básico paso a paso", expanded=True):
        st.markdown("""
        Una conducción de PVC (K = 1×10⁻⁶ m) debe transportar:
        
        - **Caudal:** 80 L/s
        - **Diámetro:** 200 mm
        - **Longitud:** 2,500 m
        
        **Calcular:**
        a) Velocidad del flujo
        b) Número de Reynolds y régimen
        c) Factor de fricción (iterando hasta convergencia)
        d) Pérdidas totales por fricción
        """)
        
        if st.checkbox("Ver solución - Ejercicio 1"):
            st.success("""
            **Solución:**
            
            **a) Velocidad:**
            - Q = 80 L/s = 0.08 m³/s
            - A = π·(0.2/2)² = 0.0314 m²
            - V = Q/A = 0.08 / 0.0314 = 2.546 m/s
            
            **b) Reynolds y régimen:**
            - Re = V·D / ν = 2.546 × 0.2 / (1×10⁻⁶) = 509,200
            - Régimen: **TURBULENTO** (Re > 4,000)
            
            **c) Factor de fricción (Iterativo):**
            - Iteración 1 (Swamme Jain): f₀ ≈ 0.01185
            - Iteración 2 (Colebrook-White): f₁ ≈ 0.01183
            - Diferencia: 0.00002 < 0.0001 -> **CONVERGE**
            - **f final = 0.01183**
            
            **d) Pérdidas por Darcy-Weisbach:**
            - hf = f · (L/D) · (V²/2g)
            - hf = 0.01183 × (2500/0.2) × (2.546²/(2×9.81))
            - hf = 0.01183 × 12,500 × 0.3297
            - **hf ≈ 48.7 metros**
            
            **Interpretacion:** Se pierden aproximadamente 48.7 metros de presion
            en los 2.5 km de conducción.
            """)
    
    # Ejercicio 2
    with st.expander("**Ejercicio 2:** Comparación de diámetros"):
        st.markdown("""
        Un municipio necesita transportar 100 L/s a 3 km de distancia con pérdidas máximas de 10 m.
        
        ¿Qué diámetro mínimo de tubería PVC se requiere?
        
        (Sugerencia: Prueba con D = 250, 280 y 300 mm)
        """)
        
        if st.checkbox("Ver solución - Ejercicio 2"):
            st.success("""
            **Solución:**
            
            Probando diferentes diámetros con Q = 100 L/s, L = 3000 m:
            
            **D = 250 mm:**
            - V = 2.037 m/s
            - Re = 407,400 (Turbulento)
            - f ≈ 0.01195
            - hf ≈ 15.8 m (Excede 10 m)
            
            **D = 280 mm:**
            - V = 1.620 m/s
            - Re = 324,000 (Turbulento)
            - f ≈ 0.01205
            - hf ≈ 9.2 m (Cumple!)
            
            **D = 300 mm:**
            - V = 1.415 m/s
            - Re = 283,000 (Turbulento)
            - f ≈ 0.01210
            - hf ≈ 6.8 m (Cumple con margen)
            
            **Respuesta:** Diámetro mínimo recomendado: **280 mm**
            (con pérdidas de 9.2 m, muy cerca del límite de 10 m)
            """)
    
    # Ejercicio 3
    with st.expander("**Ejercicio 3:** Caudal máximo con pérdidas limitadas"):
        st.markdown("""
        Una tubería de PVC de 150 mm de diámetro y 4 km de longitud 
        debe cumplir con una restricción: pérdidas máximas de 5 metros.
        
        ¿Cuál es el caudal máximo que puede transportar?
        
        (Sugerencia: Prueba con Q = 20, 30 y 40 L/s)
        """)
        
        if st.checkbox("Ver solución - Ejercicio 3"):
            st.success("""
            **Solución:**
            
            Probando diferentes caudales con D = 150 mm, L = 4000 m:
            
            **Q = 20 L/s:**
            - V = 1.131 m/s
            - Re = 169,650 (Turbulento)
            - hf ≈ 1.8 m
            
            **Q = 30 L/s:**
            - V = 1.698 m/s
            - Re = 254,550 (Turbulento)
            - hf ≈ 3.9 m
            
            **Q = 35 L/s:**
            - V = 1.981 m/s
            - Re = 297,200 (Turbulento)
            - hf ≈ 5.3 m (Excede 5 m)
            
            **Q = 33 L/s:**
            - V = 1.868 m/s
            - Re = 280,200 (Turbulento)
            - hf ≈ 4.8 m (Cumple)
            
            **Respuesta:** Caudal máximo: **33 L/s** (con pérdidas de 4.8 m)
            """)
    
    # Ejercicio 4
    with st.expander("**Ejercicio 4:** Presión disponible después de conducción"):
        st.markdown("""
        Un tanque elevado (100 m de altura) alimenta una red de distribución a través 
        de una conducción:
        
        - **Diámetro:** 200 mm
        - **Longitud:** 1,500 m
        - **Caudal:** 50 L/s
        - **Rugosidad:** K = 1×10⁻⁶ m
        
        Calcular la presión disponible al final de la conducción (en metros de columna de agua).
        
        (Considerar que Presión_final = Presión_inicial - hf)
        """)
        
        if st.checkbox("Ver solución - Ejercicio 4"):
            st.success("""
            **Solución:**
            
            **Paso 1: Calcular pérdidas (hf)**
            - Q = 50 L/s = 0.05 m³/s
            - A = π·(0.2/2)² = 0.0314 m²
            - V = 0.05 / 0.0314 = 1.592 m/s
            - Re = 1.592 × 0.2 / (1×10⁻⁶) = 318,400 (Turbulento)
            - f ≈ 0.01201 (iterativo)
            - hf = 0.01201 × (1500/0.2) × (1.592²/(2×9.81))
            - hf ≈ 11.8 m
            
            **Paso 2: Calcular presión disponible**
            - Presión inicial (altura del tanque): 100 m
            - Pérdidas por fricción: 11.8 m
            - **Presión disponible = 100 - 11.8 = 88.2 metros**
            
            **Resultado:** Se dispone de **88.2 m de presion** en el punto final.
            Esto es suficiente para cualquier sistema de distribución urbano típico.
            """)
