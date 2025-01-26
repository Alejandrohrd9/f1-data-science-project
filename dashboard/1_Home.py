import streamlit as st

st.set_page_config(page_title="Inicio", page_icon="🏁")
st.title('🏁 Bienvenidos al dashboard de la Fórmula 1')

st.write("""Este dashboard interactivo proporciona un análisis  de las competiciones de Fórmula 1, permitiendo explorar datos sobre circuitos, temporadas y carreras a través de visualizaciones dinámicas. 
A través de tres secciones, podrás acceder a mapas y gráficos que te permitirán visualizar el desarrollo de una temporada de Fórmula 1.""")

st.write("## Secciones:")
st.write("### 1. Circuitos:")
st.write("""En esta sección, podrás explorar la ubicación de los circuitos con dos mapas interactivos que muestran las posiciones de los circuitos a lo largo de los años, desde el 2000,
y su distribución geográfica.""")

st.write("### 2. Temporadas:")
st.write("""En la sección de temporadas, encontrarás gráficos sobre el transcurso de la temporada, distribuyéndose de la siguiente manera:""")
st.markdown("""
**- Clasificación por pilotos y constructores:** Observa cómo avanzan las posiciones en la clasificación a lo largo de la temporada, tanto a nivel de pilotos como de constructores.\n
**- Distribución de victorias y pódiums:** Realiza una comparación de las victorias y pódiums obtenidos por los pilotos.
""")

st.write("### 3. Carreras:")
st.write("""Aquí encontrarás análisis más detallados de cada carrera, donde podrás visualizar:""")
st.markdown("""
**- Gráficos de cambios de posición:** Observa cómo cambian las posiciones a lo largo de una carrera y conoce también las posiciones ganadas y/o perdidas por los pilotos considerando la posición inicial y final.\n
**- Análisis de stints:** Visualiza las estratégias de neumáticos que ha seguido cada piloto y cuál ha sido el número de vueltas promedio por neumático para evaluar sus características.\n
**- Tiempos de vuelta:** Analiza cómo se distribuyen las vueltas de cada piloto por tiempo para sacar conclusiones en cuanto a rendimiento y cómo de consistentes son.\n
**- Tiempos de pitstops:** Analiza el rendimiento de cada equipo durante las paradas en boxes y la consistencia en sus tiempos de ejecución.
""")


