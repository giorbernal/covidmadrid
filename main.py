import sys
import os
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from utils.helper import loadCovidData, plotPlaces, transformCoordenate, checkPositions

prefix = os.environ['APP_PATH']

if sys.version_info[0] < 3:
    reload(sys) # noqa: F821 pylint:disable=undefined-variable
    sys.setdefaultencoding("utf-8")

#@st.cache
def get_data(dataset='muni'):
    df = loadCovidData(prefix=prefix, dataset=dataset)
    return df

def drawEvolution(df, places, agg_factor, dataset='muni'):
    data_acc, data_day = plotPlaces(df, places, agg_factor=agg_factor, dataset=dataset, plot=False)
    data_acc_pivoted = data_acc.pivot(index='fecha', columns='municipio_distrito', values='Contagios totales')
    data_data_day_pivoted = data_day.pivot(index='fecha', columns='municipio_distrito', values='Contagios diarios')

    st.subheader("Contagios totales")

    st.write(data_acc_pivoted.T)
    chart = (
        alt.Chart(data_acc)
            .mark_line()
            .encode(
            x="fecha:N",
            y="Contagios totales:Q",
            color="municipio_distrito:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)

    st.subheader("Contagios por día")

    st.write(data_data_day_pivoted.T)
    chart = (
         alt.Chart(data_day)
         .mark_line()
         .encode(
             x="fecha:N",
             y="Contagios diarios:Q",
             color="municipio_distrito:N",
         )
     )
    st.altair_chart(chart, use_container_width=True)

# Main Screen
st.title('Evolución de Covid-19 en la Comunidad de Madrid')
st.text('Compare la situación en diferentes puntos de la comunidad de Madrid')

df = get_data()

# Sidebar Configuration
st.sidebar.title('Configuración de la Visualización')
places = st.sidebar.multiselect(
    "Elija un municipio/distrito", list(df['municipio_distrito'].unique()), ['Madrid-Centro']
)
agg_factor = st.sidebar.slider("Agrupación de datos por N días:", 1, 7, 1)
zones_enabled = st.sidebar.checkbox(label='¿Quieres ver evolución en tu zona?', value=False)

if len(places) > 0:
    drawEvolution(df, np.array(places), agg_factor=agg_factor)
else:
    st.warning("Seleccione al menos un municipio/distrito o active la visualización por zona")

if zones_enabled:
    st.subheader("Contagios por día en la zona seleccionada")
    lat = st.slider('Latitud(º)', 39.863371338285305, 41.17038447781618, 40.4165001, 0.005)
    long = st.slider('Longitud(º)', -4.592285156249999, -3.05419921875, -3.7025599, 0.005)
    long_tx, lat_tx = transformCoordenate(long, lat)
    zone = checkPositions([(long_tx,lat_tx)], prefix=prefix)
    if len(zone) > 0:
        df_zones = get_data(dataset='zonas')
        df_amp = pd.DataFrame(
            data=np.array([float(lat), float(long)]).reshape(1,2),
            columns=['lat', 'lon'])
        st.map(df_amp, zoom=8)
        drawEvolution(df_zones, np.array(zone), agg_factor, dataset='zonas')
    else:
        st.error('Zona desconocida o fuera de la Comunidad de Madrid!')
