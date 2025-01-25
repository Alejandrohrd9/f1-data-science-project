import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Temporadas", page_icon="🏁")
st.title('🏁 Clasificaciones y Distribuciones de la Temporada de F1')
st.markdown("""En esta página podrás explorar las clasificaciones completas de los pilotos y constructores durante una temporada específica, considerando los puntos obtenidos en carreras regulares como en carreras al sprint. 
Además, podrás analizar como se han distribuído los podiums y las victorias entre los pilotos para esa temporada""")

# Función para cargar el conjunto de datos
def load_data(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, file_path)
    results_data = pd.read_csv(data_path)
    return results_data

# Colores para los constructores
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

# Cargar conjunto de datos que contiene los resultados de las pruebas
results_data = load_data('../../data/race_and_sprint_results_2000-2024.csv')
seasons = sorted(results_data['season'].unique(), reverse=True)

# Selector de temporada
selected_season = st.selectbox(
    "Seleccione una temporada:",
    seasons,
    index=None,
)
st.write("Temporada:", selected_season)


if selected_season:
    ## Clasificación de pilotos ##
    st.subheader("Clasificación pilotos", divider="gray")
    st.markdown("""Este gráfico de líneas muestra la evolución de puntos obtenidos por piloto a lo largo de la temporada.""")

    # Order by season, round, driverId
    results_data = results_data.sort_values(by=['season', 'round', 'driverId'])

    # Calcular el número de puntos obtenidos por piloto en cada fin de semana
    results_data['cumulative_points'] = results_data.groupby(['season','driverId'])['weekendPoints'].cumsum()

    # Filtrar por temporada
    season_df = results_data[results_data['season'] == selected_season]
    season_df['driverFullName'] = season_df['driverName'] + " " + season_df['driverSurname']

    # Obtener el valor máximo por piloto
    sorted_drivers = season_df.groupby('driverFullName')['cumulative_points'].max().sort_values(ascending=False).index

    # Crear gráfico con plotly. Gráfico de líneas
    fig = px.line(season_df, 
        x='circuitName', 
        y='cumulative_points', 
        color='driverFullName', 
        markers=True, 
        title=f'Puntos ganados por piloto en cada carrera para la temporada {selected_season}',
        labels={'circuitName': 'Gran Premio', 'cumulative_points': 'Puntos Ganados', 'driverFullName': 'Pilotos'},
        category_orders={'driverFullName': sorted_drivers} # Ordenar por puntos ganados
    )  

    # Ajustar más detalles gráfico
    fig.update_layout(
        height=600, 
        legend=dict(
            title="Piloto",
            x=1,  
            y=1
        )
    )

    # Mostrar gráfico con Streamlit
    st.plotly_chart(fig)


    ## Clasificación de constructores ##    
    st.subheader("Clasificación constructores", divider="gray")
    st.markdown("""Este gráfico de barras muestra la evolución de puntos obtenidos por constructores a lo largo de la temporada, a partir de los puntos conseguidos por los pilotos.""")

    # Preparar conjunto de datos
    columns_for_constructos = ['season', 'constructorId', 'constructorName', 'constructorNationality', 'points', 'weekendPoints']
    filtered_constructors_df = season_df[columns_for_constructos].copy()

    # Agrupar por constructor y seleccionamos los puntos obtenidos
    grouped_constructors_df = filtered_constructors_df.groupby(['season','constructorId', 'constructorName'])['weekendPoints'].sum().reset_index()
    ordered_constructors_df = grouped_constructors_df.sort_values(by='weekendPoints', ascending=False)

    # Crear gráfico de barras
    fig_constructors = px.bar(
        ordered_constructors_df, 
        x='weekendPoints', 
        y='constructorName', 
        orientation='h', # Barras horizontales
        title=f'Clasificación de constructores para la temporada {selected_season}',
        labels={'weekendPoints': 'Puntos', 'constructorName': 'Constructores'},
        color='constructorName',
        color_discrete_map=constructor_color_dict,
        category_orders={'constructorName': ordered_constructors_df} # Ordernar por puntos 
    )
    # Mostrar gráfico con Streamlit
    st.plotly_chart(fig_constructors)


    ### Victorias y podiums ###
    st.subheader("Distribución de victorias y podiums", divider="gray")
    st.markdown("""En esta sección se muestra con detalle en un primer gráfico, las victorias obtenidas por pilotos, y en un segundo gráfico, los pilotos que han subido más veces al podium para una temporada.""")

    ## Victorias
    # Los siguientes gráficos se muestran en formato columna
    wins_podiums_col_1, wins_podiums_col_2 = st.columns(2)
    # Filtrar para obtener las filas cuyo position sea igual a 1, de este modo se obtienen las victorias
    wins = season_df[season_df['position'] == 1]
    # Obtener número de victorias por piloto
    grouped_wins = wins.groupby(['driverCode', 'driverName', 'driverSurname']).size().reset_index(name='Wins')
    grouped_wins = grouped_wins.sort_values(by='Wins', ascending=False)
    grouped_wins['driverFullName'] = grouped_wins['driverName'] + " " + grouped_wins['driverSurname']

    # Crear gráfico Pie
    fig = px.pie(
        grouped_wins,
        names='driverCode',
        values='Wins',
        title="Distribución de victorias por piloto",
        hole=0.2
    )
    
    # Ajustar gráfico
    fig.update_layout(
        height=350
    )
    # Mostrar gráfico en la primera columna dentro de la págia
    with wins_podiums_col_1:
        st.plotly_chart(fig)


    ## Podiums: position < 4
    # Filtrar para obtener las filas cuyo position sea igual inferior a 4 para obtener las filas cuyas posiciones correspondan a las de podium
    podiums = season_df[season_df['position'] < 4]
    # Obtener número de podiums por piloto
    grouped_podiums = podiums.groupby(['driverCode', 'driverName', 'driverSurname']).size().reset_index(name='Podiums')
    grouped_podiums = grouped_podiums.sort_values(by='Podiums', ascending=False)
    grouped_podiums['driverFullName'] = grouped_podiums['driverName'] + " " + grouped_podiums['driverSurname']
    
    # Crear gráfico Pie
    fig = px.pie(
        grouped_podiums,
        names='driverCode',  
        values='Podiums',  
        title="Distribución de podiums por piloto",
        hole=0.2
    )

    # Ajustar gráfico
    fig.update_layout(
        height=350
    )
    # Mostrar gráfico en la segunda columna dentro de la págia
    with wins_podiums_col_2:
        st.plotly_chart(fig)