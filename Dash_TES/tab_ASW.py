import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

##################################################################################################
#Load the data and create the plots
##################################################################################################
#Importar curvas cero cupón en pesos históricas
df_CCC_TESPESOS = pd.read_csv('D:/andrgome/Documents/BDPython/TESPESOS.csv',encoding='latin-1')
df_CCC_TESPESOS = df_CCC_TESPESOS.T #Transponer la base de datos
df_CCC_TESPESOS.index = pd.to_datetime(df_CCC_TESPESOS.index)

#Importar IRS
df_BDMercado = pd.read_csv('D:/andrgome/Documents/BDPython/BDMercado.csv',encoding='latin-1')
df_SWAPS = pd.DataFrame()
df_SWAPS['IBR2Y'] = df_BDMercado['CLSWIB2 Curncy'].astype(float)
df_SWAPS['IBR5Y'] = df_BDMercado['CLSWIB5 Curncy'].astype(float)
df_SWAPS['IBR10Y'] = df_BDMercado['CLSWIB10 Curncy'].astype(float)
df_SWAPS['Fecha'] = pd.to_datetime(df_BDMercado['FECHA'])
df_SWAPS.set_index('Fecha', inplace=True)
df_SWAPS['IBR2Y'] = (1+df_SWAPS['IBR2Y']/400)**4-1
df_SWAPS['IBR5Y'] = (1+df_SWAPS['IBR5Y']/400)**4-1
df_SWAPS['IBR10Y'] = (1+df_SWAPS['IBR10Y']/400)**4-1

df_yearly = pd.DataFrame()
df_yearly['1Y'] = df_CCC_TESPESOS[1*365]/100
df_yearly['2Y'] = df_CCC_TESPESOS[2*365]/100
df_yearly['3Y'] = df_CCC_TESPESOS[3*365]/100
df_yearly['4Y'] = df_CCC_TESPESOS[4*365]/100
df_yearly['5Y'] = df_CCC_TESPESOS[5*365]/100
df_yearly['6Y'] = df_CCC_TESPESOS[6*365]/100
df_yearly['7Y'] = df_CCC_TESPESOS[7*365]/100
df_yearly['8Y'] = df_CCC_TESPESOS[8*365]/100
df_yearly['9Y'] = df_CCC_TESPESOS[9*365]/100
df_yearly['10Y'] = df_CCC_TESPESOS[10*365]/100

#Esta es una rutina para convertir tasas cero cupón en tasas par. Se basa en el concepto que una tasa par
#se obtiene de un bono que tiene precio 100 y se descuenta cada año a las tasas cero cupón correspondientes.

lista_FD_COP = []
df_Tasas_Par = pd.DataFrame()
last_column_TESTF = df_CCC_TESPESOS.shape[0]-1

for i in range(1,last_column_TESTF):

    for j in range (1,11):
        item = 1/(1+df_CCC_TESPESOS[365*j][i]/100)**j
        lista_FD_COP.append(item)

    df_FD_COP = pd.DataFrame(lista_FD_COP)
    df_FD_COP = df_FD_COP.rename(columns={0: 'FD'})
    df_FD_COP['Tao'] = 1
    df_FD_COP['CUMPROD']=(df_FD_COP['FD']).cumsum()
    df_FD_COP['Tasa Par']=(1-df_FD_COP['FD'])/ df_FD_COP['CUMPROD']

    nombre = df_CCC_TESPESOS.index[i].strftime("%m/%d/%Y")
    df_Tasas_Par[nombre] = df_FD_COP['Tasa Par']
    lista_FD_COP = []

df_Tasas_Par2 = df_Tasas_Par.T[[1,4,9]]
df_Tasas_Par2 = df_Tasas_Par2.rename(columns={1: 'PAR_TES2Y',4: 'PAR_TES5Y',9: 'PAR_TES10Y'})
df_Tasas_Par2.index.names = ['Fecha']
df_Tasas_Par2.index = pd.to_datetime(df_Tasas_Par2.index)

df_ASW = df_Tasas_Par2.merge(df_SWAPS, on='Fecha')
df_ASW[pd.to_numeric(df_ASW['IBR2Y'], errors='coerce').notnull()]
df_ASW[pd.to_numeric(df_ASW['IBR5Y'], errors='coerce').notnull()]
df_ASW[pd.to_numeric(df_ASW['IBR10Y'], errors='coerce').notnull()]
df_ASW['ASWS2Y'] = df_ASW['PAR_TES2Y']-df_ASW['IBR2Y']
df_ASW['ASWS5Y'] = df_ASW['PAR_TES5Y']-df_ASW['IBR5Y']
df_ASW['ASWS10Y'] = df_ASW['PAR_TES10Y']-df_ASW['IBR10Y']



#Create the scatter plot:
Scatter_Fig=px.scatter()
Scatter_Fig.add_scatter(x=df_ASW.index, y=df_ASW["ASWS2Y"],name='2Y',marker_size=6, marker_color='dimgrey', line_color='dimgrey',line_width=1)
Scatter_Fig.add_scatter(x=df_ASW.index, y=df_ASW["ASWS5Y"],name='5Y',marker_size=6, marker_color='gold', line_color='gold',line_width=1)
Scatter_Fig.add_scatter(x=df_ASW.index, y=df_ASW["ASWS10Y"],name='10Y',marker_size=6, marker_color='darkblue', line_color='darkblue',line_width=1)

Scatter_Fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
},yaxis=dict(tickformat=".2%"))


#Create Layout
tab_ASW_layout = html.Div([
    html.H2("ASWS TES vs IBR", id='title'), #Creates the title of the app
#    dcc.Dropdown(id="emisor_dropdown",options=[{ 'label':l,'value':l} for l in emisor],value=['ISAGEN']),
    dcc.Graph(figure=Scatter_Fig, id='Scatter'),
    html.Div(id='page-ASW-content')    
])

