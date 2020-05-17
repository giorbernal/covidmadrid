import sys
import os
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from utils.helper import loadCovidData, plotPlaces, transformCoordenate, checkPositions, sample_coordinates, top_places

prefix = os.environ['APP_PATH']

modes = ['Total','Municipo/Distrito','Detalle de municipio','Mapa']

if sys.version_info[0] < 3:
    reload(sys) # noqa: F821 pylint:disable=undefined-variable
    sys.setdefaultencoding("utf-8")

@st.cache(ttl=7200)
def get_data(dataset='muni'):
    df = loadCovidData(prefix=prefix, dataset=dataset)
    return df

def drawEvolution(df, places, agg_factor, dataset='muni'):
    data_acc, data_day = plotPlaces(df, places, agg_factor=agg_factor, dataset=dataset, plot=False)
    data_acc_pivoted = data_acc.pivot(index='fecha', columns='municipio_distrito', values='Contagios totales')
    data_data_day_pivoted = data_day.pivot(index='fecha', columns='municipio_distrito', values='Contagios diarios')

    st.markdown("### Contagios totales")

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

    st.markdown("### Contagios por día")

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
st.markdown('# Evolución de Covid-19 en la Comunidad de Madrid')

df = get_data()

# Sidebar Configuration
st.sidebar.title('Configuración de la Visualización')
agg_factor = st.sidebar.slider("Agrupación de datos por N días:", 1, 7, 1)

mode = st.sidebar.selectbox("Elija modo de visualizacion:", modes)

if mode == modes[0]:
    st.markdown('## Evolución total de los casos')
    df_total = df.groupby(by='fecha_informe').sum().reset_index()
    unique_place = 'Comunidad de Madrid'
    df_total['municipio_distrito'] = df_total.apply(lambda x: unique_place, axis=1)
    drawEvolution(df_total, np.array([unique_place]), agg_factor=agg_factor)

    st.markdown('## Situación reciente en las zonas más poblados')
    last_days = st.slider("Casos acumulados en los últimos N días:", 1, 7, 1)
    _, df_inc_top = plotPlaces(df, top_places, agg_factor=1, plot=False)
    dates_to_select = df_inc_top['fecha'].unique()[::-1][0:last_days]
    df_inc_top_filtered = df_inc_top[df_inc_top['fecha'].isin(dates_to_select)]
    df_inc_top_filtered_agg = df_inc_top_filtered.groupby(by='municipio_distrito').sum().reset_index()

    chart = (
        alt.Chart(df_inc_top_filtered_agg)
        .mark_bar()
        .encode(y='municipio_distrito', x='Contagios diarios')
    )
    st.altair_chart(chart, use_container_width=True)

elif mode == modes[1]:
    st.markdown('## Compare la situación en diferentes lugares')
    places = st.multiselect(
        "Elija un municipio/distrito", list(np.sort(df['municipio_distrito'].unique())), ['Madrid-Centro']
    )
    if len(places) > 0:
        drawEvolution(df, np.array(places), agg_factor=agg_factor)
    else:
        st.warning("Seleccione al menos un municipio/distrito")

elif mode == modes[3]:
    st.markdown('## Contagios por día en la zona seleccionada')
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

elif mode == modes[2]:
    st.markdown('## Analice el detalle del municipio')
    city_detail = st.selectbox('Seleccione Municipio para observar el detalle:', list(sample_coordinates.keys()))
    zones = checkPositions(sample_coordinates[city_detail], prefix=prefix)
    df_zones = get_data(dataset='zonas')
    drawEvolution(df_zones, np.array(zones), agg_factor, dataset='zonas')

st.sidebar.markdown('([GitHub](https://github.com/giorbernal/covidmadrid))')
