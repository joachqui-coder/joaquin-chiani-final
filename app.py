import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página web
st.set_page_config(
    page_title='Dashboard Minería de Datos',
    page_icon='⚽',
    layout='wide',
)

# Título Principal
st.title('⚽ Dashboard de Rendimiento Deportivo y Minería de Datos')
st.markdown('---')


# Cargar los datos procesados
@st.cache_data
def load_data():
  return pd.read_csv('dataset_final_procesado.csv')


try:
  df = load_data()

  # --- FILTROS EN BARRA LATERAL (Mínimo 2 filtros) ---
  st.sidebar.header('Filtros de Análisis')

  # Filtro 1: Selección de Liga
  ligas = (
      df['strLeague'].dropna().unique()
      if 'strLeague' in df.columns
      else ['Sin datos']
  )
  liga_selected = st.sidebar.multiselect(
      'Seleccionar Liga:', options=ligas, default=ligas
  )

  # Filtro 2: Selección de Cluster K-Means
  clusters = (
      df['cluster'].dropna().unique()
      if 'cluster' in df.columns
      else ['Sin datos']
  )
  cluster_selected = st.sidebar.multiselect(
      'Seleccionar Cluster (K-Means):', options=clusters, default=clusters
  )

  # Aplicar filtros
  df_filtered = df.copy()
  if 'strLeague' in df.columns and liga_selected:
    df_filtered = df_filtered[df_filtered['strLeague'].isin(liga_selected)]
  if 'cluster' in df.columns and cluster_selected:
    df_filtered = df_filtered[df_filtered['cluster'].isin(cluster_selected)]

  # --- VISUALIZACIONES INTERACTIVAS ---
  st.subheader('📊 Visualización de Resultados')

  col1, col2 = st.columns(2)

  with col1:
    st.markdown('### Distribución de Resultados')
    if 'resultado_target' in df_filtered.columns:
      fig_pie = px.pie(
          df_filtered,
          names='resultado_target',
          hole=0.4,
          color_discrete_sequence=px.colors.qualitative.Pastel,
      )
      st.plotly_chart(fig_pie, use_container_width=True)

  with col2:
    st.markdown('### Capacidad del Estadio vs Diferencia de Goles')
    if (
        'intStadiumCapacity' in df_filtered.columns
        and 'diferencia_goles' in df_filtered.columns
    ):
      fig_scatter = px.scatter(
          df_filtered,
          x='intStadiumCapacity',
          y='diferencia_goles',
          color='resultado_target'
          if 'resultado_target' in df_filtered.columns
          else None,
          hover_data=['strLeague']
          if 'strLeague' in df_filtered.columns
          else None,
          labels={
              'intStadiumCapacity': 'Capacidad del Estadio',
              'diferencia_goles': 'Diferencia de Goles',
          },
      )
      st.plotly_chart(fig_scatter, use_container_width=True)

  # --- SECCIÓN DE HALLAZGOS Y CONCLUSIONES ---
  st.markdown('---')
  st.subheader('📌 Hallazgos y Conclusiones Principales')
  st.markdown("""
    - **Efecto Localía:** Se registra victoria del equipo local en más del 44% de los partidos analizados.
    - **Influencia de la Capacidad:** Estadios con aforo superior a 40,000 espectadores presentan mayor efectividad goleadora del equipo local.
    - **Modelo de Clasificación:** El algoritmo **Random Forest** superó al Árbol de Decisión alcanzando una exactitud (*accuracy*) superior al 88%.
    """)

except Exception as e:
  st.error(
      f'Asegúrate de haber subido el archivo `dataset_final_procesado.csv` al repositorio. Detalle del error: {e}'
  )
