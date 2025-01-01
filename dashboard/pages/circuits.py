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

fig = px.scatter_mapbox(
    circuits_data,
    lat='latitude',
    lon='longitude'
)
fig.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig)

# colored_circuits_data = circuits_data.copy()

# colored_circuits_data['color'] = ['red' if val == colored_circuits_data['season'].max() else 'blue' for val in colored_circuits_data['season']]
# st.map(colored_circuits_data, latitude=colored_circuits_data['latitude'], longitude=colored_circuits_data['longitude'])

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


    