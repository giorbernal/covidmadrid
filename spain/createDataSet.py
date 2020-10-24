import numpy as np
import pandas as pd

def adaptField(df, field):
    df[field + '_f'] = df[field].apply(lambda x: float(str(x).replace(',','.').replace('%','')))
    df.drop(labels=[field], axis=1, inplace=True)

df_press=pd.read_csv('datasets/press.csv')
df_test=pd.read_csv('datasets/test.csv')
df_cases=pd.read_csv('datasets/cases.csv')

#Fix column name
df_cases.columns=['Fecha', 'cod_ine', 'CCAA', 'num_casos', 'num_casos_prueba_pcr',
       'num_casos_prueba_test_ac', 'num_casos_prueba_otras',
       'num_casos_prueba_desconocida']

res = df_cases.merge(df_press,how='outer', on=['Fecha','cod_ine','CCAA'], suffixes=['_cases','_press']).merge(df_test,how='outer', on=['Fecha','cod_ine','CCAA'], suffixes=['','_test'])
res.drop(labels=['Column','Column2','Column3','Column4','Column5','Column6','Column7','Column8'], axis=1, inplace=True)

adaptField(res,'PCR_x_1000hab.')
adaptField(res,'TEST_Acc')
adaptField(res,'Total_Pruebas_x_1000hab.')
adaptField(res,'OTROS_TESTS_x_1000hab.')
adaptField(res,'% Camas Ocupadas COVID')
adaptField(res,'% Camas Ocupadas UCI COVID')

res.to_csv('datasets/covid19_CCAA.csv', sep=';', decimal=',', index=False)

df_press.to_csv('datasets/press_ft.csv', sep=';', decimal=',', index=False)
df_test.to_csv('datasets/test_ft.csv', sep=';', decimal=',', index=False)
df_cases.to_csv('datasets/cases_ft.csv', sep=';', decimal=',', index=False)
