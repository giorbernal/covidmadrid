# Covid-19 Madrid

This is an analysis of Covid-19 impact in the area of Madrid (Spain).

The source of the information is provided directly by "La Comunidad de Madrid", organizing the datasets by [place](https://datos.comunidad.madrid/catalogo/dataset/covid19_tia_muni_y_distritos) and by [health zone](https://datos.comunidad.madrid/catalogo/dataset/covid19_tia_zonas_basicas_salud).

## Analysis in notebooks

On one hand, the information will be shown in the notebook [CovidMadrid](notebooks/CovidMadrid.ipynb) and a more detailed visualization for certain places will be shown in [ZonesDetail](notebooks/ZonesDetail.ipynb).

Additionally, in the notebook [TopHealthZones](notebooks/TopHealthZones.ipynb) you can see the rate incidence in Health Basic Zones,

## Web application

On the other hand, the framework [streamlit](https://www.streamlit.io) has been used to develop a web application and visualize, in an interactive mode, some of the graphs shown in the previous notebooks. The configuration of this application has been saved in the attached [Dockerfile](Dockerfile). The main code is such application is located [here](main.py).

Additional configuration has been included to deploy the application in [heroku](https://www.heroku.com) environment. You can see the result in this [link](https://covidmadrid.herokuapp.com).
