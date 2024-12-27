import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Race results [2000-2024]')

def load_data():
    results_data = pd.read_csv('data/cleaned_results_2000-2024.csv')
    return results_data

results_data = load_data()

# Order by season, round, driverId
results_data = results_data.sort_values(by=['season', 'round', 'driverId'])

# Calculate accumulated by drivers per season
results_data['cumulative_points'] = results_data.groupby(['season','driverId'])['points'].cumsum()

# Filter data for season 2024
df_2024 = results_data[results_data['season'] == 2024]

# Display the line chart with Streamlit's native plot
st.title("Puntos Ganados por Piloto en Cada Carrera")
st.write("Este gráfico muestra los puntos ganados por piloto en cada carrera de la temporada 2024.")

# Plotting using Plotly Express
fig = px.line(df_2024, 
              x='circuitId', 
              y='cumulative_points', 
              color='driverId', 
              markers=True, 
              title='Puntos Ganados por Piloto en Cada Carrera',
              labels={'circuitId': 'Carrera', 'cumulative_points': 'Puntos Ganados', 'driverId': 'Piloto'})

# Display the plot in Streamlit
st.plotly_chart(fig)