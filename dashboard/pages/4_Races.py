import os
import streamlit as st
import pandas as pd
import requests
import fastf1
import fastf1.plotting
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Page setup
st.set_page_config(page_title="Carreras", page_icon="🏁")
st.title('🏁 Detalles de carrera')
st.markdown(""" 
    Aquí puedes encontrar una análisis detallado de carrera. A través de los gráficos se ofrece una visión exhastiva del rendimiendo de los pilotos durante la carrera. Puede encontrar aspectos como:
    -  Evolución de la posición de los pilotos por vuelta 
    -  Ganancia y pérdida de posiciones por piloto 
    -  Estrategia de neumáticos utilizada durante la carrera 
    -  Número medio de vueltas por neumáticos utilizado durante la carrera 
    -  Tiempos de vuelta por pilotos y cómo de consistente han sido 
    -  Tiempos de pitstops 
""")
# Selector de temporada
# Selector de GP

# Gráfico de stints (a partir del 2011)
# Gráfico de paradas en boxes 

def load_data(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, file_path)
    results_data = pd.read_csv(data_path)
    return results_data

# Function to convert duration to seconds
def duration_to_seconds(duration):
    duration_str = str(duration)
    if ':' in duration_str: 
        minutes, seconds_miliseconds = duration_str.split(':')
        seconds, miliseconds = seconds_miliseconds.split('.')
        return int(minutes) * 60 + int(seconds) + int(miliseconds) / 1000
    else:  
        return float(duration_str)

circuits_data = load_data('../../data/cleaned_circuits_2000-2024.csv')

selected_round = ''
selected_season = ''

# Constructor color mapping
constructor_color_dict = {
    'Alfa Romeo': '#9C2D2C',      
    'AlphaTauri': '#1E1E1E',     
    'Alpine F1 Team': '#0070BB', 
    'Aston Martin': '#006F42',    
    'Caterham': '#006747',       
    'Ferrari': '#DC0000',         
    'Force India': '#5F4B8B',     
    'Haas F1 Team': '#666666',   
    'HRT': '#F2A900',              
    'Lotus F1': '#1E1E1E',        
    'Lotus': '#F4E300',           
    'Manor Marussia': '#E60012',  
    'Marussia': '#A00000',       
    'McLaren': '#FF5700',         
    'Mercedes': '#00D2BE',        
    'Racing Point': '#F9A9D5',    
    'RB F1 Team': '#1E41FF',      
    'Red Bull': '#1E41FF',        
    'Renault': '#FFCD00',        
    'Sauber': '#003A5C',          
    'Toro Rosso': '#1E41FF',      
    'Virgin': '#E10000',          
    'Williams': '#0046A3'         
}

### Filtering by season ###
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

if selected_season and selected_round and st.button("Cargar datos"):

    ### Request to FastF1 ###
    session = fastf1.get_session(selected_season, selected_round, 'R')
    session.load()
    laps = session.laps

    drivers = session.drivers
    drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]

    results = session.results

    # Crear dataframe con posiciones sólo
    positions = results[["DriverNumber", "Abbreviation", "GridPosition", "Position"]]
    positions['PositionChange'] = positions["GridPosition"] - positions["Position"]
    positions_list = positions['Abbreviation'].to_list()

    ### Posiciones carrera por vuelta ###
    st.subheader("Posiciones de los pilotos por vuelta", divider="gray")
    st.markdown("""Este gráfico de líneas muestra la evolución de la posición en carrera de los piloto a lo largo de las vueltas.""")
    laps_updated = laps.drop(columns=['Time', 'PitOutTime', 'PitInTime', 'FastF1Generated', 'FreshTyre', 'IsAccurate', 'Deleted', 'DeletedReason'], axis=1)
    laps_sorted = laps_updated.sort_values(by="Position")

    fig = px.line(
        laps_updated,
        x='LapNumber',
        y='Position',
        color='Driver',
        markers=False,
        color_discrete_sequence=px.colors.qualitative.Set1,
        category_orders={"Driver": laps_sorted["Driver"].tolist()},  # Orden personalizado
        title="Tiempo de vueltas por piloto (Ordenados por posición final)"
    )

    fig.update_traces(
        line=dict(width=2)
    )

    fig.update_layout(
        xaxis_title="Número de Vuelta",
        yaxis_title="Posición",
        yaxis=dict(autorange="reversed"),
        template="plotly_white",
        legend_title="Pilotos",
        height=600,
        width=1000
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)

    ### Diferencia posición de salida - posición final ###
    st.subheader("Cambios de posición", divider="gray")
    st.markdown("""Este gráfico de barras permite visualizar las posiciones ganadas y perdidas en carrera a partir de la posición inicial.""")
    position_changes = positions.groupby(['DriverNumber', 'Abbreviation'])['PositionChange'].mean().reset_index()

    fig = px.bar(
        position_changes,
        x='PositionChange',
        y='Abbreviation',
        color='PositionChange',
        orientation='h',
        category_orders={'Driver': positions_list},  # Ordenar por posiciones finales
        title="Ganancia o Pérdida de Posiciones por Piloto",
        labels={'PositionChange': 'Cambios de posiciones'}
    )
    fig.update_layout(
        height=800,
        legend_title="Cambios de posición",
        xaxis_title="Número de posiciones",
        yaxis_title="Piloto"
    )
    # Mostrar el gráfico
    st.plotly_chart(fig)

    ### Stints ###
    st.subheader("Estrategia de neumáticos", divider="gray")
    st.markdown("""En esta sección se muestran dos gráficos que aportan información sobre los neumáticos utilizados en carrera.
    Un primer gráfico de barras horizontales con el que se puede visualizar el uso de neumáticos por parte de cada piloto durante la carrera, en función de los diferentes stints.
    La longitud de la barra refleja la cantidad de vueltas que el piloto ha recorrido con un determinado compuesto de neumático.
    El segundo gráfico, es un gráfico de barras verticales que muestra el uso promedio de neumáticos en la carrera, agrupado por tipo de compuesto.""")
    stint_col_1, stint_col_2 = st.columns(2)
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
                marker=dict(color=compound_color),
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

    fig.update_layout(
        title=f"{selected_race} {selected_season}",
        height=800,
        xaxis_title="Número de vuelta",
        yaxis_title="Piloto",
        barmode='stack',  # Las barras se apilan horizontalmente
        xaxis=dict(showgrid=False, zeroline=False),  # Ocultar líneas de rejilla
        yaxis=dict(autorange="reversed"),  # Invertir el orden de los pilotos
        template='plotly_white',
        legend_title='Compuestos'
    )
    # Mostrar los gráficos en columnas
    with stint_col_1:
        st.plotly_chart(fig)

    # Media de número de vueltas por compuesto
    laps_per_stint_compound = laps_sorted.groupby(['Driver', 'Stint', 'Compound'])['LapNumber'].count().reset_index()
    laps_per_stint_compound.rename({'LapNumber': 'LapCount'}, inplace=True)
    
    laps_compound_mean_df = laps_per_stint_compound.groupby('Compound')['LapNumber'].mean().reset_index()
    
    # Diccionario con los colores a partir del set
    compound_colors = {compound: color for compound, color in compounds_set}

    fig = px.bar(
        laps_compound_mean_df,
        x='Compound',
        y='LapNumber',
        color='Compound',
        title=f'Número de vueltas por compuesto y stint',
        labels={'LapNumber': 'Número de vueltas', 'Compound': 'Compuesto', 'Stint': 'Tanda'},
        color_discrete_map=compound_colors
    )
    with stint_col_2:
        st.plotly_chart(fig)

    ### Laps ###
    st.subheader('Distribución de Tiempos de Vuelta por piloto', divider='gray')
    st.markdown("""Dos gráficos que permiten analiazar los tiempos de vuelta durante el transcurso de un Gran Premio. 
    Un primer gráfico de dispersión que muestra cómo los tiempos de vuelta de cada piloto se distribuyen a lo largo de las diferentes vueltas de la carrera, y un segundo gráfico de boxplot
    que muestra la distribución de los tiempos de vuelta de los pilotos a lo largo de una carrera.
    """)

    lap_col_1, lap_col_2 = st.columns(2)
    laps_updated['LapTimeSeconds'] = laps_updated['LapTime'].dt.total_seconds()

    fig = px.scatter(
        laps_updated,
        x='LapNumber',
        y='LapTimeSeconds',
        color='Driver',
        title="Consistencia de Tiempos por Vuelta",
        labels={"LapNumber": "Número de vuelta", "LapTimeSeconds": "Tiempo por vuelta en segundos"},
        hover_data=['Compound']
    )

    fig.update_traces(marker=dict(size=6, opacity=0.8))

    fig.update_layout(
        template="plotly_white",
        height=600,
        width=900,
        legend_title='Pilotos'

    )
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Box plot
    fig = px.box(
        laps_updated,
        x='Driver',
        y='LapTimeSeconds',
        category_orders={'Driver': positions_list},  # Ordenar por posiciones finales
        hover_data=['LapNumber'],  # Mostrar el número de vuelta en el hover
        color='Driver',  # Usar colores por piloto
        title='Análisis de Tiempos de Vuelta por Piloto'
    )

    fig.update_layout(
        xaxis_title="Piloto",
        yaxis_title="Tiempo por vuelta en segundos",
        legend_title='Pilotos'       
    )
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    ### Pitstops ###
    st.subheader('Distribución de Tiempos de Pitstop por constructor', divider='gray')
    st.markdown("""Este gráfico permite identificar rápidamente qué constructores tienen una mayor consistencia en sus pitstops y cuáles experimentan más variabilidad o tiempos de parada más largos en general.""")
    pitstops_df = load_data('../../data/cleaned_pitstops.csv')
    pitstops_df['duration'] = pitstops_df['duration'].apply(lambda duration: duration_to_seconds(duration))

    fig = px.violin(
        pitstops_df[(pitstops_df['season'] == selected_season) & (pitstops_df['round'] == selected_round)],
        x='constructorName',
        y='duration',
        color='constructorName',
        color_discrete_map=constructor_color_dict,
        box=True,
        points="all",
        hover_data=['constructorName', 'duration', 'lap', 'driverFullName'],
        
    )
    fig.update_layout(
        title="Tiempos de pitstop",
        xaxis_title="Constructor",
        yaxis_title="Duración en segundos",
        legend_title='Constructores'
    )
    fig.update_traces(quartilemethod="exclusive")
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)