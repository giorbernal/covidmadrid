import sys
import numpy as np
import altair as alt
import streamlit as st
from utils.helper import loadCovidData, plotPlaces

if sys.version_info[0] < 3:
    reload(sys) # noqa: F821 pylint:disable=undefined-variable
    sys.setdefaultencoding("utf-8")

#@st.cache
def get_UN_data():
    df = loadCovidData(prefix='/Users/bernal/Documents/ext/GitRepos/covidmadrid/')
    return df

st.title('Evolución de Covid-19 en la Comunidad de Madrid')
st.text('Compare la situación en diferentes puntos de la comunidad de Madrid')

st.sidebar.title('Parámetros de configuración')

df = get_UN_data()

places = st.sidebar.multiselect(
    "Elija un municipio/distrito", list(df['municipio_distrito'].unique()), ["Getafe", "Leganés"]
)
if not places:
    st.error("Por favor, seleccione al menos un municipio o disctrito.")
    #return

agg_factor = st.sidebar.slider("Agrupación de datos por N días:", 1, 7, 1)

st.subheader("Contagios totales")

data_acc, data_day = plotPlaces(df, np.array(places), agg_factor=agg_factor, plot=False)
data_acc_pivoted = data_acc.pivot(index='fecha',columns='municipio_distrito',values='Contagios totales')
data_data_day_pivoted = data_day.pivot(index='fecha',columns='municipio_distrito',values='Contagios diarios')

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

