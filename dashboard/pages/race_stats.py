import streamlit as st
import pandas as pd
import requests
import fastf1
import fastf1.plotting
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Race stats",
)
st.title('Detalles de carrera')


# Selector de temporada
# Selector de GP

# Gráfico de stints (a partir del 2011)
# Gráfico de paradas en boxes 

def load_data():
    results_data = pd.read_csv('../data/cleaned_circuits_2000-2024.csv')
    return results_data

circuits_data = load_data()

selected_round = ''
selected_season = ''

# Filtering by season
seasons = sorted(circuits_data['season'].unique(), reverse=True)
selected_season = st.selectbox(
    "Seleccione una temporada:",
    seasons,
    index=None,
)

if selected_season:
    races = circuits_data[circuits_data['season'] == selected_season]
    selected_race = st.selectbox(
        "Seleccione un gran premio:",
        races['raceName'],
    )
    selected_round = races[races['raceName'] == selected_race]['round'].values[0]

if selected_season and selected_round and st.button("Load data"):
    session = fastf1.get_session(selected_season, selected_round, 'R')
    session.load()
    laps = session.laps

    drivers = session.drivers

    drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]

    results = session.results
    positions = results[["DriverNumber", "GridPosition", "Position"]]

    stints = laps[["Driver", "DriverNumber", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "DriverNumber", "Stint", "Compound"])
    stints = stints.count().reset_index()

    stints = stints.rename(columns={"LapNumber": "StintLength"})


    stints_with_position = pd.merge(stints, positions, on=['DriverNumber'], how='left')
    stints_with_position = stints_with_position.astype({'Position':'int64', 'GridPosition':'int64'})
    stints_with_position = stints_with_position.sort_values(by=['Position', 'Stint'])


    # Crear una figura en Plotly
    fig = go.Figure()

    compounds_set = set()
    # Iterar por cada piloto
    for driver in drivers:

        driver_stints = stints_with_position.loc[stints["Driver"] == driver].copy()

        driver_stints[['Stint', 'Compound']] = driver_stints[['Stint', 'Compound']].replace('nan', np.nan)
        driver_stints[['Stint', 'Compound']] = driver_stints[['Stint', 'Compound']].bfill()
        
        previous_stint_end = 0
        for _, row in driver_stints.iterrows():
            # Obtener el color correspondiente al compuesto
            compound_color = fastf1.plotting.get_compound_color(row["Compound"], session=session)
            compounds_set.add((row["Compound"],compound_color))

            # Añadir una barra horizontal para cada stint del piloto
            fig.add_trace(go.Bar(
                y=[driver],  # Eje Y muestra al piloto
                x=[row["StintLength"]],  # Eje X es la duración del stint
                base=previous_stint_end,  # El inicio de la barra
                orientation='h',  # Barras horizontales
                marker=dict(color=compound_color),  # Colores y bordes
                name=row["Compound"],  # Nombre del compuesto para el hover,
                hovertemplate=(
                    f"Piloto: {driver}<br>" +
                    f"Compuesto: {row['Compound']}<br>" +
                    f"Duración del stint: {row['StintLength']} vueltas<br>" +
                    f"Inicia en la vuelta: {previous_stint_end}<br>"+
                    f"Posicion inicial: {row['GridPosition']}<br>"+
                    f"Posicion final: {row['Position']}<br>"
                ),
                showlegend=False 
            ))

            previous_stint_end += row["StintLength"]
        
    for compound, color in compounds_set:
        fig.add_trace(go.Bar(
            y=[None],  # Para no mostrar una barra visible, solo usar la leyenda
            x=[0],  # Valor de 0 para que no se dibuje una barra visible
            name=compound,  # Nombre de la entrada de la leyenda
            marker=dict(color=color),  # El color correspondiente al compuesto
            showlegend=True  # Mostrar una entrada en la leyenda para cada compuesto
    ))

    # Configuración del diseño
    fig.update_layout(
        title=f"{selected_race} {selected_season}",
        height=800,
        xaxis_title="Lap Number",
        yaxis_title="Driver",
        barmode='stack',  # Las barras se apilan horizontalmente
        xaxis=dict(showgrid=False, zeroline=False),  # Ocultar líneas de rejilla
        yaxis=dict(autorange="reversed"),  # Invertir el orden de los pilotos
        template='plotly_white'  # Tema blanco limpio
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)