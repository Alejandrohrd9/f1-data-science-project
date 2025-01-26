import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Circuits", page_icon="🏁")
st.title('🏁 Circuitos')
st.markdown("""En esta página se puede visualizar los circuitos que han acogido un Gran Premio de Fórmula 1 desde la temporada 2000. En un primer mapa se muestran todos los circuitos,
resaltando los de la temporada 2024, y un segundo mapa que, tras filtrar por temporada, muestra los circuitos correspondientes a la temporada seleccionada.""")

# Función para cargar el conjunto de datos
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '../../data/cleaned_circuits_2000-2024.csv')
    results_data = pd.read_csv(data_path)
    return results_data

# Cargar datos
circuits_data = load_data()

st.subheader("Circuitos desde la temporada del 2000", divider="gray")
st.markdown("""En el siguiente mapa se muestran los circuitos que han formado parte del calendario de la Formula 1 desde el año 2000, y se resaltan los circuitos donde ha habido Gran Premio para la última temporada 2024""")

# Dataframe para el mapa, añadiendo una nueva columna que permita posteriormente diferenciar en el mapa los grandes premios del 2024 y el histórico.
colored_circuits_data = circuits_data.copy()
colored_circuits_data['color'] = ['2024' if val == colored_circuits_data['season'].max() else 'Histórico (a partir del 2000)' for val in colored_circuits_data['season']]

# Crear mapa con plotly
fig = px.scatter_mapbox(
    colored_circuits_data,
    lat='latitude',
    lon='longitude',
    mapbox_style='open-street-map', # Estilo de mapa
    hover_name='circuitName', # Agregar el nombre del circuito al hover
    color_discrete_map={
        'Histórico (a partir del 2000)': 'red',
        '2024': 'green'
    }, #Establecer colores
    color='color',    
    zoom=1,
    center=dict(lat=51.0057, lon=13.7274), # Posición inicial en el mapa
    custom_data=['season', 'country'] # Columnas a usar en el hover
)

# Contenido para el hover
fig.update_traces(
    hovertemplate=(
        "<b>Circuito:</b> %{hovertext}<br>"  # hovertext proviene de hover_name (circuitName)
        "<b>Temporada:</b> %{customdata[0]}<br>"  # customdata[0] es 'season'
        "<b>País:</b> %{customdata[1]}<br>"  # customdata[1] es 'country'
        "<extra></extra>"
    )
)

# Ajustar más detalles mapa
fig.update_layout(
    title="Mapa con los circuitos a partir de la temporada de 2000",
    legend_title_text="Años de los circuitos"
)
# Mostrar mapa con Streamlit
st.plotly_chart(fig)


st.subheader("Circuitos por temporada", divider="gray")
# Lista de temporadas para el selector
seasons = sorted(circuits_data['season'].unique())
# Selector de temporada
selected_season = st.selectbox(
    "Seleccione una temporada:",
    seasons,
    index=None,
)

# Label con tmeporada seleccionada
st.write("Temporada:", selected_season)
if selected_season:
    st.markdown("""En el siguiente mapa se muestran los circuitos que forman parte del calendario de carreras para la temporada seleccionada""")
    circuits_season_df = circuits_data[circuits_data['season'] == selected_season] # Crear dataframe para la temporada seleccionada
    fig = px.scatter_mapbox( 
        circuits_season_df,
        lat='latitude',
        lon='longitude',
        hover_name='circuitName',  # Agregar el nombre del circuito al hover
        zoom=1,
        mapbox_style='open-street-map',  # Estilo del mapa
        custom_data=['country'], # Columnas a usar en el hover
        center=dict(lat=51.0057, lon=13.7274) # Posición inicial en el mapa
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Circuito:</b> %{hovertext}<br>"  # hovertext proviene de hover_name (circuitName)
            "<b>País:</b> %{customdata[0]}<br>"  # customdata[1] es 'country'
            "<extra></extra>"
        )
    )

    # Ajustar más detalles mapa
    fig.update_layout(
        title=f"Circuitos para la temporada {selected_season}"
    )

    # Mostrar el mapa con Streamlit
    st.plotly_chart(fig)

    