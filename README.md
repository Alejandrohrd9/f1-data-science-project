# Proyecto de visualización y análisis de datos sobre la F1

Este repositorio contiene un proyecto de ciencia de datos que utiliza datos de F1 para realizar:
1. **Obtención y visualización de datos:** Extracción, procesamiento y exploración de datos sobre carreras, pilotos, circuitos, resultados y pitstops.
2. **Dashboard interactivo con Streamlit:** Dashboard para visualizar los datos de manera interactiva
3. **Machine Learning:** Un notebook con implementación de modelos predictivos para predecir datos.

## Estructura del proyecto
```
Proyecto/
├── data/                 # Archivos de datos utilizados (CSVs)
├── notebooks/            # Jupyter Notebooks para extracción, procesamiento y visualización de los datos. También Jupyter Notebooks para trabajar con modelos ML
├── dashboard/            # Código fuente del dashboard Streamlit
├── README.md             # Documentación del repositorio
├── requirements.txt      # Dependencias del proyecto
├── .gitignore            # Archivos y carpetas ignorados por Git
```

## Características Principales

## Requisitos

- Python >= 3.8
- Bibliotecas necesarias (detalladas en `requirements.txt`):
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - plotly
  - scikit-learn
  - streamlit

### Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/Alejandrohrd9/f1-data-science-project
   ```

2. Navega al directorio del proyecto:
   ```bash
   cd f1-data-science-project
   ```

3. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta el dashboard o los notebooks.
Para iniciar el dashboad, ejecuta el siguiente comando:
```bash
streamlit run dashboard/1_Home.py
```

## Dashboard en streamlit
https://f1-data-science-project-qnayh2cri98a8xgtmymmvw.streamlit.app/