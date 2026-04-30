import streamlit as st
import sys
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Sanitaria I - Libro Interactivo",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .chapter-header {
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Importar módulos de capítulos
from capitulos import capitulo_1, capitulo_2

# Diccionario de capítulos
CAPITULOS = {
    "📚 Inicio": None,
    #"1️⃣ Fundamentos de Sanitaria": capitulo_1,
    "2️⃣ Línea Piezométrica y Pérdidas": capitulo_2,
    # "3️⃣ Abastecimiento de Agua": capitulo_3,
    # "4️⃣ Alcantarillado": capitulo_4,
    # "5️⃣ Tratamiento de Aguas Residuales": capitulo_5,
}

# Barra lateral
st.sidebar.title("📖 Tabla de Contenidos")
capitulo_seleccionado = st.sidebar.radio(
    "Selecciona un capítulo:",
    options=CAPITULOS.keys(),
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tip:** Usa las pestaña de la izquierda para navegar entre capítulos. "
    "Cada capítulo contiene ejercicios interactivos y cálculos automáticos."
)

# Contenido principal
if capitulo_seleccionado == "📚 Inicio":
    st.markdown("<h1 class='main-title'>💧 Sanitaria I</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='main-title'>Libro Interactivo con Streamlit</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Contenidos")
        st.write("""
        - Caudal de diseño
        - Captación lateral
        - Captación de fondo
        - Linea piezométrica y 
        - Pérdidas por fricción
        - Pérdias menores
        - Diseño de aducción
        """)
    
    with col2:
        st.markdown("### 🔧 Herramientas")
        st.write("""
        - Calculadoras interactivas
        - Gráficos en tiempo real
        - Simuladores de diseño
        - Ejercicios prácticos
        """)
    
    with col3:
        st.markdown("### 🎯 Objetivos")
        st.write("""
        - Aprender conceptos clave
        - Resolver problemas prácticos
        - Diseñar sistemas sanitarios
        - Aplicar normas (RAS 2017)
        """)
    
    st.markdown("---")
    st.markdown("""
    ### ¿Cómo usar este libro?
    
    1. **Selecciona un capítulo** en la barra lateral izquierda
    2. **Lee el contenido teórico** con ejemplos
    3. **Interactúa con los calculadores** para entender mejor
    4. **Resuelve los ejercicios** propuestos
    5. **Experimenta con diferentes valores** para ver cómo cambian los resultados
    
    Cada capítulo está diseñado para ser autodidacta pero también puede ser usado en clase.
    """)
    
else:
    # Cargar el módulo del capítulo seleccionado
    modulo_capitulo = CAPITULOS[capitulo_seleccionado]
    if modulo_capitulo:
        modulo_capitulo.render()