import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit as st
from utils.helper import loadCovidData, loadCovidDataSpain, getMadridTotalData, getLastUpdate, plotPlaces, transformCoordenate, checkPositions, sample_coordinates, top_places
from utils.RatePerZone import plotFilteredBy, loadZonesDataSet, ZONES, ZONES_WITH_INDEX, RATE_ACTIVE_14, RATE_14
from utils.RNN import RNN, getPlaceSerie

prefix = os.environ['APP_PATH']

modes = ['Total','Municipo/Distrito','Detalle de municipio','Mapa','Incidencia por ZBS']

if sys.version_info[0] < 3:
    reload(sys) # noqa: F821 pylint:disable=undefined-variable
    sys.setdefaultencoding("utf-8")

@st.cache(ttl=7200)
def get_data(dataset='muni_s'):
    df = loadCovidData(prefix=prefix, dataset=dataset)
    if dataset.startswith('muni'):
        df_spain = loadCovidDataSpain(prefix=prefix)
    else:
        df_spain = pd.DataFrame()
    return df, df_spain

def drawEvolution(df, places, agg_factor, dataset='muni_s'):
    data_acc, data_day = plotPlaces(df, places, agg_factor=agg_factor, dataset=dataset, plot=False)
    data_acc_pivoted = data_acc.pivot(index='fecha_str', columns='municipio_distrito', values='Contagios totales')
    data_data_day_pivoted = data_day.pivot(index='fecha_str', columns='municipio_distrito', values='Contagios semanales')

    st.markdown("### Contagios totales")

    st.write(data_acc_pivoted.T)
    chart = (
        alt.Chart(data_acc)
            .mark_line()
            .encode(
            x="fecha:T",
            y="Contagios totales:Q",
            color="municipio_distrito:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("### Contagios por semana")

    st.write(data_data_day_pivoted.T)
    chart = (
         alt.Chart(data_day)
         .mark_line()
         .encode(
             x="fecha:T",
             y="Contagios semanales:Q",
             color="municipio_distrito:N",
         )
     )
    st.altair_chart(chart, use_container_width=True)

def handleSeriePrediction(df, place, agg_factor, dataset='muni_s'):
    pass
    # if st.checkbox("Análisis predictivo"):
    #     serie = getPlaceSerie(df, place, agg_factor, dataset)
    #     st.markdown("#### Parámetros de la RNN")
    #     window_size = st.number_input(label='window size (2-14)', min_value=2, max_value=14, value=7)
    #     lstm_units = st.number_input(label='LSTM units (1-64)', min_value=1, max_value=64, value=8)
    #     epochs = st.number_input(label='epochs (10-200)', min_value=10, max_value=200, value=150)
    #
    #     if st.button('Predicción'):
    #         with st.spinner('Entrenando modelo ...'):
    #             rnn = RNN(data=serie, window_size=window_size, lstm_units=lstm_units, epochs=epochs)
    #             history, score = rnn.train(verbose=2)
    #         st.success('Hecho!')
    #
    #         # plot history
    #         st.markdown("#### Curvas de aprendizaje")
    #         plt.plot(history.history['loss'], label='train')
    #         plt.plot(history.history['val_loss'], label='test')
    #         plt.legend()
    #         st.pyplot()
    #
    #         st.markdown("#### Realidad Vs Modelo Predictivo")
    #         y, y_pred = rnn.getAllPredictions()
    #         plt.plot(y, 'b', label='Realidad')
    #         plt.plot(y_pred, 'r', label='Modelo Predictivo')
    #         plt.legend()
    #         st.pyplot()
    #         st.markdown("#### Predicción a 30 dias")
    #         preds = rnn.predict(30)
    #         plt.plot(preds)
    #         st.pyplot()

# Main Screen
st.markdown('# Evolución de Covid-19 en la Comunidad de Madrid')

df, df_spain = get_data()

# Sidebar Configuration
st.sidebar.title('Configuración de la Visualización')
# with muni_s dataset data comes already grouped each 7 days
#agg_factor = st.sidebar.slider("Agrupación de datos por N días:", 1, 7, 1)
agg_factor = 1

mode = st.sidebar.selectbox("Elija modo de visualizacion:", modes)

if mode == modes[0]:
    st.markdown('## Evolución total de los casos')
    df_all_madrid = getMadridTotalData(df, df_spain)
    last_update = getLastUpdate(df_all_madrid)
    st.text('última actualización: ' + str(last_update))
    places = st.multiselect(
        "Elija un índice total", list(df_all_madrid['municipio_distrito'].unique()), ['Comunidad de Madrid']
    )
    if len(places) > 0:
        drawEvolution(df_all_madrid, np.array(places), agg_factor=agg_factor)
        if (len(places)==1):
            handleSeriePrediction(df_all_madrid, places[0], agg_factor)
    else:
        st.warning("Seleccione al menos una opción")

    st.markdown('## Situación reciente en las zonas más poblados')
    last_weeks = st.slider("Casos acumulados en las últimas semanas:", 1, 4, 1)
    _, df_inc_top = plotPlaces(df, top_places, agg_factor=1, plot=False)
    dates_to_select = df_inc_top['fecha'].unique()[::-1][0:last_weeks]
    df_inc_top_filtered = df_inc_top[df_inc_top['fecha'].isin(dates_to_select)]
    df_inc_top_filtered_agg = df_inc_top_filtered.groupby(by='municipio_distrito').sum().reset_index()

    chart = (
        alt.Chart(df_inc_top_filtered_agg)
        .mark_bar()
        .encode(y='municipio_distrito', x='Contagios semanales')
    )
    st.altair_chart(chart, use_container_width=True)

elif mode == modes[1]:
    st.markdown('## Compare la situación en diferentes lugares')
    places = st.multiselect(
        "Elija un municipio/distrito", list(np.sort(df['municipio_distrito'].unique())), ['Madrid-Centro']
    )
    if len(places) > 0:
        drawEvolution(df, np.array(places), agg_factor=agg_factor)
        if (len(places)==1):
            handleSeriePrediction(df, places[0], agg_factor)
    else:
        st.warning("Seleccione al menos un municipio/distrito")

elif mode == modes[3]:
    st.markdown('## Contagios por día en la zona seleccionada')
    lat = st.number_input('Latitud(º)', 39.863371338285305, 41.17038447781618, 40.4165001, 0.005)
    long = st.number_input('Longitud(º)', -4.592285156249999, -3.05419921875, -3.7025599, 0.005)
    long_tx, lat_tx = transformCoordenate(long, lat)
    zone = checkPositions([(long_tx,lat_tx)], prefix=prefix)
    if len(zone) > 0:
        df_zones, _ = get_data(dataset='zonas_s')
        df_amp = pd.DataFrame(
            data=np.array([float(lat), float(long)]).reshape(1,2),
            columns=['lat', 'lon'])
        st.map(df_amp, zoom=8)
        drawEvolution(df_zones, np.array(zone), agg_factor, dataset='zonas_s')
        handleSeriePrediction(df_zones, zone[0], agg_factor, dataset='zonas_s')
    else:
        st.error('Zona desconocida o fuera de la Comunidad de Madrid!')

elif mode == modes[2]:
    st.markdown('## Analice el detalle del municipio')
    city_detail = st.selectbox('Seleccione Municipio para observar el detalle:', list(sample_coordinates.keys()))
    zones = checkPositions(sample_coordinates[city_detail], prefix=prefix)
    df_zones, _ = get_data(dataset='zonas_s')
    drawEvolution(df_zones, np.array(zones), agg_factor, dataset='zonas_s')

elif mode == modes[4]:
    selected = loadZonesDataSet(prefix)
    st.markdown('## Tasa de incidencia en los últimos 14 dias por ZBS')
    N = st.slider('Seleccione el numero N de ZBS con mas incidencia:', 40, 150, 60, 10)
    orderByName = st.checkbox('Ordenar por nombre', False)
    if orderByName:
        yParam=ZONES
    else:
        yParam=ZONES_WITH_INDEX

    top = plotFilteredBy(selected, RATE_14, N)
    chart = (
        alt.Chart(top)
        .mark_bar()
        .encode(y=yParam, x=RATE_14)
    )
    st.altair_chart(chart, use_container_width=True)

    topActive = plotFilteredBy(selected, RATE_ACTIVE_14, N)
    chart = (
        alt.Chart(topActive)
        .mark_bar()
        .encode(y=yParam, x=RATE_ACTIVE_14)
    )
    st.altair_chart(chart, use_container_width=True)

    restricted = ['Puerta Bonita', 'Vista Alegre', 'Guayaba', 'Doctor Cirajas', 'Gandhi', 'Daroca', 'La Elipa',
                  'Entrevías', 'Martínez de la Riva', 'San Diego', 'Numancia', 'Peña Prieta', 'Pozo del Tío Raimundo',
                  'Ángela Uriarte', 'Alcalá de Guadaira', 'Federica Montseny', 'Almendrales', 'Las Calesas', 'Zofío',
                  'Orcasur', 'San Fermín', 'Villa de Vallecas', 'San Andrés', 'San Cristóbal', 'El Espinillo',
                  'Los Rosales', 'Alcobendas-Chopera', 'Miraflores', 'Alicante', 'Cuzco', 'Francia', 'Las Margaritas',
                  'Sánchez Morate', 'Humanes de Madrid', 'San Blas', 'Isabel II', 'Reyes Católicos']

    # Set thresholds
    last_days_rate_active_th = topActive[RATE_ACTIVE_14].min()
    last_days_rate_th = top[RATE_14].min()
    selected_bi = selected[selected[RATE_14] > last_days_rate_th][selected[RATE_ACTIVE_14] > last_days_rate_active_th]
    selected_bi.reset_index(drop=True, inplace=True)

    st.text(str(selected_bi.shape[0]) + ' zonas se ajustan a los umbrales mínimos a la vez')

    selected_bi['restricted'] = selected_bi[ZONES].apply(lambda x: x in restricted)
    selected_bi_rest = selected_bi[selected_bi['restricted']]
    selected_bi_rest.reset_index(drop=True, inplace=True)
    selected_bi_miss = selected_bi[~selected_bi['restricted']]
    selected_bi_miss.reset_index(drop=True, inplace=True)
    st.text('¿Cuantas zones restringidas están en estos umbrales? ' + str(selected_bi_rest.shape[0]))

    fig = plt.figure(figsize=[20, 20])
    for i in np.arange(selected_bi_rest.shape[0]):
        plt.annotate(selected_bi_rest[ZONES][i], xy=(selected_bi_rest[RATE_14][i], selected_bi_rest[RATE_ACTIVE_14][i]))
    for i in np.arange(selected_bi_miss.shape[0]):
        plt.annotate(selected_bi_miss[ZONES][i], xy=(selected_bi_miss[RATE_14][i], selected_bi_miss[RATE_ACTIVE_14][i]))
    plt.plot(selected_bi_rest[RATE_14], selected_bi_rest[RATE_ACTIVE_14], 'or', selected_bi_miss[RATE_14],
             selected_bi_miss[RATE_ACTIVE_14], 'o', mew=5, )
    plt.legend(['zonas restringidas', 'zonas NO restringidas'])
    plt.xlabel(RATE_14)
    plt.ylabel(RATE_ACTIVE_14)
    st.pyplot(fig)

st.sidebar.markdown('([GitHub](https://github.com/giorbernal/covidmadrid))')
