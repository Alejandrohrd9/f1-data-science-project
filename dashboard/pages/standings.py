import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
        page_title="Standings",
)
st.title('Clasificaciones')

def load_data():
    results_data = pd.read_csv('data/cleaned_results_2000-2024.csv')
    return results_data

results_data = load_data()

seasons = sorted(results_data['season'].unique())

selected_season = st.selectbox(
    "Seleccione una temporada:",
    seasons,
    index=None,
)

st.write("Temporada:", selected_season)

if selected_season:
    ## Drivers ##
    # Order by season, round, driverId
    results_data = results_data.sort_values(by=['season', 'round', 'driverId'])

    # Calculate accumulated by drivers per season
    results_data['cumulative_points'] = results_data.groupby(['season','driverId'])['points'].cumsum()

    # Filter data for season 2024
    season_df = results_data[results_data['season'] == selected_season]

    st.title(f"Clasificaciones para la temporada {selected_season}")
    st.subtitle(f"Este gráfico muestra los puntos ganados por piloto en cada carrera de la temporada {selected_season}.")

    # Plotting using Plotly Express
    fig = px.line(season_df, 
                x='circuitId', 
                y='cumulative_points', 
                color='driverId', 
                markers=True, 
                title='Puntos Ganados por Piloto en Cada Carrera',
                labels={'circuitId': 'Carrera', 'cumulative_points': 'Puntos Ganados', 'driverId': 'Piloto'})

    # Display the plot in Streamlit
    st.plotly_chart(fig)


    ## Constructors ##
    st.subtitle(f"Este gráfico muestra la clasificación de constructores en la temporada {selected_season}.")
    
    columns_for_constructos = ['season', 'constructorId', 'constructorName', 'constructorNationality', 'points']
    filtered_constructors_df = season_df[columns_for_constructos].copy()

    grouped_constructors_df = filtered_constructors_df.groupby(['season','constructorId', 'constructorName'])['points'].sum().reset_index()
    ordered_constructors_df = grouped_constructors_df.sort_values(by='points', ascending=True)

    fig_constructors = px.bar(
        ordered_constructors_df, 
        x=ordered_constructors_df['points'], 
        y=ordered_constructors_df['constructorName'], 
        orientation='h',
        labels={'points': 'Points', 'constructorName': 'Constructor'}
    )
    # Display the plot in Streamlit
    st.plotly_chart(fig_constructors)