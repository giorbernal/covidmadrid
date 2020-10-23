import numpy as np
import pandas as pd

def adaptField(df, field):
    df[field + '_f'] = df[field].apply(lambda x: float(str(x).replace(',','.').replace('%','')))
    df.drop(labels=[field], axis=1, inplace=True)

df_press=pd.read_csv('datasets/press.csv')
df_test=pd.read_csv('datasets/test.csv')
df_cases=pd.read_csv('datasets/cases.csv')

res = df_cases.merge(df_press,how='outer', on=['Fecha','cod_ine','CCAA'], suffixes=['_cases','_press']).merge(df_test,how='outer', on=['Fecha','cod_ine','CCAA'], suffixes=['','_test'])
res.drop(labels=['Column','Column2','Column3','Column4','Column5','Column6','Column7','Column8','Column_test','Column2_test','Column3_test','Column4_test','Column5_test','Column6_test','Column7_test','Column8_test'], axis=1, inplace=True)

adaptField(res,'PCR_x_1000hab.')
adaptField(res,'TEST_Acc')
adaptField(res,'Total_Pruebas_x_1000hab.')
adaptField(res,'OTROS_TESTS_x_1000hab.')
adaptField(res,'Total_Pruebas_x_1000hab._test')
adaptField(res,'% Camas Ocupadas COVID')
adaptField(res,'% Camas Ocupadas UCI COVID')
adaptField(res,'PCR_x_1000hab._test')
adaptField(res,'TEST_Acc_test')
adaptField(res,'OTROS_TESTS_x_1000hab._test')

res.to_csv('datasets/covid19_CCAA.csv', sep=';', decimal=',', index=False)

df_press.to_csv('datasets/press_ft.csv', sep=';', decimal=',', index=False)
df_test.to_csv('datasets/test_ft.csv', sep=';', decimal=',', index=False)
df_cases.to_csv('datasets/cases_ft.csv', sep=';', decimal=',', index=False)
