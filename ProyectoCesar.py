import streamlit as st
import calendar
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"

df = pd.read_csv("Datos/FC25_Stats.csv")

#Paso a lista de forma unica
list_nacionalidades = df['Nacionalidad'].unique().tolist()
list_ligas = df['Liga'].unique().tolist()
list_teams = df['Club'].unique().tolist()

# Selectbox para filtrar
with st.sidebar:
    filtro_pais = st.selectbox(
        "País:",
        list_nacionalidades,
        index = None,
        placeholder =  "Selecciona un país"
    )

with st.sidebar:
    filtro_liga = st.selectbox(
        "Liga:",
        list_ligas,
        index = None,
        placeholder =  "Selecciona una liga"
    )

with st.sidebar:
    filtro_club = st.selectbox(
        "Club:",
        list_teams,
        index = None,
        placeholder = "Selecciona una club"
    )

df_filtrado = df.copy()

if filtro_pais != None:
    df_filtrado = df_filtrado[df_filtrado["Nacionalidad"] == filtro_pais]

if filtro_liga != None:
    df_filtrado = df_filtrado[df_filtrado["Liga"] == filtro_liga]

if filtro_club != None:
    df_filtrado = df_filtrado[df_filtrado["Club"] == filtro_club]

st.title("FC 25 FutWiz")
st.write("Lista de jugadores:")
st.dataframe(df_filtrado)

fig = px.scatter(df_filtrado, x="PMD", y="Total_stats", color="Position", size="Rating", hover_name="Name")

st.plotly_chart(fig,use_container_width=True)

st.write('Grafico de Dispersión')
fig_dispersion = px.scatter(df_filtrado, x="Position", y='Rating', hover_name="Name")
st.plotly_chart(fig_dispersion,use_container_width=True)

#Rating en FC25 
fig_histograma = px.histogram(
    df_filtrado,
    x='Rating',
    nbins=10, #numero de barras en el histograma
    title='Distribución de Ratings',
    labels={'Rating': 'Rating'},
    text_auto=True
)
st.plotly_chart(fig_histograma, use_container_width=True)

#Distribucion de jugadores
fig_pie = px.pie(df_filtrado, names='Nacionalidad', title='Distribución de Jugadores por Nacionalidad')
st.plotly_chart(fig_pie)


#grafico de barras por posicion
fig_bar_pos = px.bar(
    df_filtrado,
    x="Position",
    title="Cantidad de Jugadores por Posición",
    labels={"Position": "Posición", "count": "Cantidad"},
    text_auto=True
)
st.plotly_chart(fig_bar_pos, use_container_width=True)


#mapa de calor por nacionalidad y posicion
heatmap_data = df_filtrado.groupby(['Position', 'Nacionalidad']).size().reset_index(name='Count')
fig_heatmap = px.density_heatmap(
    heatmap_data,
    x="Position",
    y="Nacionalidad",
    z="Count",
    title="Mapa de Calor por Posición y Nacionalidad",
    labels={"Count": "Cantidad"}
)
st.plotly_chart(fig_heatmap, use_container_width=True)
