import pandas as pd

DATE='fecha_informe'
ZONES='zona_basica_salud'
ZONES_WITH_INDEX='zones_with_index'
RATE_ACTIVE_14='tasa_incidencia_acumulada_activos_ultimos_14dias'
RATE_14='tasa_incidencia_acumulada_ultimos_14dias'
RATE_TOTAL='tasa_incidencia_acumulada_total'

def loadZonesDataSet(prefix):
    df = pd.read_csv(prefix + 'datasets/covid19_tia_zonas_basicas_salud_s.csv', encoding='latin-1', sep=';')
    filtered = df[df[DATE] == df[DATE].max()]
    select = filtered[[ZONES, RATE_ACTIVE_14, RATE_14, RATE_TOTAL]]
    select['temp1'] = select[RATE_ACTIVE_14].apply(lambda x: float(x.replace(',', '.')))
    select['temp2'] = select[RATE_14].apply(lambda x: float(x.replace(',', '.')))
    select['temp3'] = select[RATE_TOTAL].apply(lambda x: float(x.replace(',', '.')))
    select.drop(labels=[RATE_ACTIVE_14, RATE_14, RATE_TOTAL], axis=1, inplace=True)
    select.columns = [ZONES, RATE_ACTIVE_14, RATE_14, RATE_TOTAL]
    return select

def plotFilteredBy(df, f, N, sortByName=False):
    top = df.sort_values(by=f, ascending=False).head(N)
    top.reset_index(drop=True, inplace=True)
    top.reset_index(drop=False, inplace=True)
    top[ZONES_WITH_INDEX] = top[['index', ZONES]].apply(lambda x: str(x[0] + 1).zfill(3) + '.-' + x[1], axis=1)
    return top