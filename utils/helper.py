import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data Functions

def loadCovidData():
    #url="https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/b2a3a3f9-1f82-42c2-89c7-cbd3ef801412/download/covid19_tia_muni_y_distritos.csv"
    #df = pd.read_csv(url, sep=';', encoding='latin-1')
    df = pd.read_csv('datasets/covid19_tia_muni_y_distritos.csv', sep=';', encoding='latin-1')
    # fixing data
    df['mun_distrito_clean']=df['municipio_distrito'].apply(lambda x: x.strip())
    df['tasa_incidencia_acumulada_total_float']=df['tasa_incidencia_acumulada_total'].str.replace(',','.').astype(float)
    df.drop(labels=['municipio_distrito','tasa_incidencia_acumulada_total'],axis=1, inplace=True)
    df.columns=['fecha_informe', 'casos_confirmados_ultimos_14dias','tasa_incidencia_acumulada_ultimos_14dias', 'casos_confirmados_totales','codigo_geometria', 'municipio_distrito','tasa_incidencia_acumulada_total_float']
    df.drop(labels=[], axis=1, inplace=True)
    return df

def filterCovidData(df_covid):
    maxDate = df_covid['fecha_informe'].unique().max()
    df_covid_filtered = df_covid[df_covid['fecha_informe']==maxDate]
    df_covid_filtered_simple = df_covid_filtered.drop(labels=['fecha_informe', 'casos_confirmados_ultimos_14dias','tasa_incidencia_acumulada_ultimos_14dias','codigo_geometria'], axis=1, inplace=False)
    return df_covid_filtered_simple

def loadPopulationData():
    df_pop_muni = pd.read_csv('datasets/municipio_comunidad_madrid.csv', sep=';', encoding='latin-1')
    df_pop_muni.drop(labels=['municipio_codigo', 'municipio_codigo_ine','nuts4_codigo', 'nuts4_nombre'], axis=1, inplace=True)
    df_pop_muni['habitantes']=df_pop_muni.apply(lambda x: x[1]*x[2], axis=1)
    df_pop_muni.columns=['municipio_distrito', 'superficie_km2', 'densidad_por_km2', 'habitantes']

    df_pop_dist = pd.read_csv('datasets/distritos_municipio_madrid.csv', sep=';', encoding='latin-1')
    df_pop_dist.drop(labels=['distrito_codigo', 'municipio_codigo','municipio_nombre'], axis=1, inplace=True)
    df_pop_dist['habitantes']=df_pop_dist.apply(lambda x: x[1]*x[2], axis=1)
    df_pop_dist['municipio_distrito']=df_pop_dist.apply(lambda x: 'Madrid-'+x[0].strip(), axis=1)
    df_pop_dist.drop(labels=['distrito_nombre'], axis=1, inplace=True)

    return pd.concat(objs=[df_pop_dist,df_pop_muni], axis=0, sort=True)

def loadResData():
    df_social = pd.read_csv('datasets/servicios_sociales_registro_centros.csv', sep=';', encoding='latin-1')
    df_res = df_social[(df_social['sector']=='Personas mayores')][['plazas_autorizadas_numero','municipio_nombre']]
    df_res_agg = df_res.groupby(by='municipio_nombre').sum()
    df_res_agg.reset_index(inplace=True)
    df_res_agg.columns=['municipio_distrito', 'plazas_autorizadas_numero']
    return df_res_agg

def loadAgeData(age_th):
    df_prof_pob_muni = pd.read_csv('datasets/cm.csv', sep=';', encoding='latin-1');
    df_prof_pob_muni['th_ind']=df_prof_pob_muni.apply(lambda x: True if (int(x[3].split()[1]))>=age_th else False, axis=1)
    df_pob_muni_older_than_th=df_prof_pob_muni[df_prof_pob_muni['th_ind']==True].drop(labels=['municipio_codigo', 'sexo','rango_edad','th_ind'], axis=1, inplace=False)
    df_pob_muni_older_than_th_agg = df_pob_muni_older_than_th.groupby(by='municipio_nombre').sum()
    df_pob_muni_older_than_th_agg.reset_index(inplace=True)
    df_pob_muni_older_than_th_agg.columns=['municipio_distrito','poblacion_older_than_th']
    return df_prof_pob_muni, df_pob_muni_older_than_th_agg

def mergeData(df_covid, df_pop, df_res, df_age_th):
    df_completed = df_covid.merge(right=df_pop,how='inner',on='municipio_distrito').merge(right=df_res,how='inner',on='municipio_distrito').merge(right=df_age_th,how='inner',on='municipio_distrito')
    df_completed['plazas_res_1000_hab']=df_completed[['plazas_autorizadas_numero','habitantes']].apply(lambda x: (x[0]/x[1])*1000, axis=1)
    df_completed['porc_poblacion_older_than_th']=df_completed[['poblacion_older_than_th','habitantes']].apply(lambda x: (x[0]/x[1])*100, axis=1)
    return df_completed

# Graph functions

def comparePlaces(df, places):
    maxDate = df['fecha_informe'].unique().max()
    df_filtered = df[(df['fecha_informe']==maxDate) & df['municipio_distrito'].isin(places)]
    
    # Casos confirmados totales
    plt.figure(figsize=(20,7))
    plt.title('Casos Totales')
    df_filtered_order_1 = df_filtered.sort_values(by='casos_confirmados_totales', ascending=0)
    sns.barplot(data=df_filtered_order_1, x='municipio_distrito', y='casos_confirmados_totales')
    plt.xlabel('Municipio - Distrito')
    plt.xticks(rotation=90)
    
    # incidencia de confirmados totales
    plt.figure(figsize=(20,7))
    plt.title('Casos Relativos a la población de la zona')
    df_filtered_order_2 = df_filtered.sort_values(by='tasa_incidencia_acumulada_total_float', ascending=0)
    sns.barplot(data=df_filtered_order_2, x='municipio_distrito', y='tasa_incidencia_acumulada_total_float')
    plt.xlabel('Municipio - Distrito')
    plt.ylabel('Casos/100000 hab.')
    plt.xticks(rotation=90)

def aggregate(x,y,group_factor):
    d=pd.DataFrame(data={'x':x,'y':y})
    d.reset_index(inplace=True)
    d['gindex']=d.apply(lambda x: int(x[0]/group_factor)*group_factor, axis=1)
    d_agg=d[['gindex','y']].groupby(by='gindex').sum()
    d_agg.reset_index(inplace=True)
    d_agg['x_red']=d_agg.apply(lambda x:d['x'].loc[x[0]],axis=1)
    d_agg.drop(labels=['gindex'],axis=1,inplace=True)
    return d_agg['x_red'],d_agg['y']
    
def plotPlaces(df, places, agg_factor=1):
    N = places.size
    plt.figure(figsize=(20,7*N))
    index=1
    for p in places:
        try:
            df_place = df[df['municipio_distrito']==p]
            df_place_sorted = df_place.sort_values(by=['fecha_informe'], ascending=1)
            x=df_place_sorted['fecha_informe']
            y=df_place_sorted['casos_confirmados_totales']            
            plt.subplot(N,2,index)
            # Total Acumulado
            plt.title(p + ' (Total Acumulado)')
            plt.ylim([(0.98)*min(y),(1.02)*max(y)])
            plt.plot(x[::agg_factor],y[::agg_factor],'r*-')
            plt.xticks(rotation=45) 
            #Incrementos por día
            x_dia=np.array(x[1:])
            y_dia=np.array(y[1:])-np.array(y[:-1])
            x_dia_red, y_dia_red = aggregate(x_dia, y_dia, agg_factor)
            plt.subplot(N,2,index+1)
            plt.title(p + ' (Incremento por día)')
            plt.bar(x_dia_red,y_dia_red, width=0.2)
            plt.xticks(rotation=45)
            index+=2
        except:
            print('Error en ' + p + '!!')

def scatterPlaces(df, x_label, y_label, reg=False):
    if (reg):
        sns.regplot(data=df,x=x_label,y=y_label)
    else:
        x = df[x_label].to_list()
        y = df[y_label].to_list()
        n = df['municipio_distrito'].to_list()

        fig, ax = plt.subplots(figsize=(15,7))
        ax.title.set_text('Relations between this two variables')
        ax.scatter(x, y)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        for i, txt in enumerate(n):
            ax.annotate(txt, (x[i], y[i]))

def showPopulationAgeProfile(df, city):
    plt.figure(figsize=(20,7))
    df_ob=df[df['municipio_nombre']==city]
    sns.barplot(data=df_ob, x='rango_edad',y='poblacion_empadronada', hue='sexo')
    plt.xticks(rotation=45)


