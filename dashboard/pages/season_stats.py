import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Standings",
)
st.title('Clasificaciones')

def load_data(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, file_path)
    results_data = pd.read_csv(data_path)
    return results_data

results_data = load_data('../../data/race_and_sprint_results_2000-2024.csv')

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


seasons = sorted(results_data['season'].unique(), reverse=True)

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
    results_data['cumulative_points'] = results_data.groupby(['season','driverId'])['weekendPoints'].cumsum()

    # Filter data for season 2024
    season_df = results_data[results_data['season'] == selected_season]
    season_df['driverFullName'] = season_df['driverName'] + " " + season_df['driverSurname']

    st.header(f"Clasificaciones para la temporada {selected_season}")

    sorted_drivers = season_df.groupby('driverFullName')['cumulative_points'].max().sort_values(ascending=False).index

    # Plotting using Plotly Express
    fig = px.line(season_df, 
                x='circuitName', 
                y='cumulative_points', 
                color='driverFullName', 
                markers=True, 
                title=f'Puntos ganados por piloto en cada carrera de la temporada {selected_season}',
                labels={'circuitName': 'Gran Premio', 'cumulative_points': 'Puntos Ganados', 'driverFullName': 'Piloto'},
                category_orders={'driverFullName': sorted_drivers})  # Sort legend by accumulated points

    fig.update_layout(
        height=600, 
        legend=dict(
            title="Piloto",
            x=1,  
            y=1
        )
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)


    #### Wins and podiums ###
    wins_podiums_col_1, wins_podiums_col_2 = st.columns(2)
    wins = season_df[season_df['position'] == 1]
    grouped_wins = wins.groupby(['driverCode', 'driverName', 'driverSurname']).size().reset_index(name='Wins')
    grouped_wins = grouped_wins.sort_values(by='Wins', ascending=False)
    grouped_wins['driverFullName'] = grouped_wins['driverName'] + " " + grouped_wins['driverSurname']
    fig = px.pie(
        grouped_wins,
        names='driverCode',
        values='Wins',
        title="Distribución de Victorias por Piloto",
        hole=0.2
    )
    fig.update_layout(
        height=350
    )
    with wins_podiums_col_1:
        st.plotly_chart(fig)


    podiums = season_df[season_df['position'] < 4]
    grouped_podiums = podiums.groupby(['driverCode', 'driverName', 'driverSurname']).size().reset_index(name='Podiums')
    grouped_podiums = grouped_podiums.sort_values(by='Podiums', ascending=False)
    grouped_podiums['driverFullName'] = grouped_podiums['driverName'] + " " + grouped_podiums['driverSurname']
    fig = px.pie(
        grouped_podiums,
        names='driverCode',  
        values='Podiums',  
        title="Distribución de Podiums por Piloto",
        hole=0.2
    )
    fig.update_layout(
        height=350
    )
    with wins_podiums_col_2:
        st.plotly_chart(fig)


    ### Constructors ###    
    columns_for_constructos = ['season', 'constructorId', 'constructorName', 'constructorNationality', 'points', 'weekendPoints']
    filtered_constructors_df = season_df[columns_for_constructos].copy()

    grouped_constructors_df = filtered_constructors_df.groupby(['season','constructorId', 'constructorName'])['weekendPoints'].sum().reset_index()
    ordered_constructors_df = grouped_constructors_df.sort_values(by='weekendPoints', ascending=False)

    fig_constructors = px.bar(
        ordered_constructors_df, 
        x='weekendPoints', 
        y='constructorName', 
        orientation='h',
        title=f'Clasificación de constructores en la temporada {selected_season}',
        labels={'weekendPoints': 'Points', 'constructorName': 'Constructor'},
        color='constructorName',
        color_discrete_map=constructor_color_dict,
        category_orders={'constructorName': ordered_constructors_df}
    )
    # Display the plot in Streamlit
    st.plotly_chart(fig_constructors)

