import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
        page_title="Circuits",
)
st.title('Circuitos')

def load_data():
    results_data = pd.read_csv('data/cleaned_circuits_2000-2024.csv')
    return results_data

circuits_data = load_data()

colored_circuits_data = circuits_data.copy()
colored_circuits_data['color'] = ['2024' if val == colored_circuits_data['season'].max() else 'Historical' for val in colored_circuits_data['season']]

fig = px.scatter_mapbox(
    colored_circuits_data,
    lat='latitude',
    lon='longitude',
    mapbox_style='carto-positron',
    hover_name='circuitName',
    color_discrete_map={
        'Historical': 'red',
        '2024': 'blue'
    },
    color='color',    
    zoom=2
)
st.plotly_chart(fig)

st.map(colored_circuits_data, latitude=colored_circuits_data['latitude'], longitude=colored_circuits_data['longitude'])

# Filtering by season
seasons = sorted(circuits_data['season'].unique())

selected_season = st.selectbox(
    "Seleccione una temporada:",
    seasons,
    index=None,
)

st.write("Temporada:", selected_season)

if selected_season:
    circuits_season_df = circuits_data[circuits_data['season'] == selected_season]
    st.map(circuits_season_df, latitude=circuits_season_df['latitude'], longitude=circuits_season_df['longitude'])


    