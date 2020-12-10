import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import median_absolute_error
from matplotlib.gridspec import  GridSpec
import pandas.tseries.converter as converter
from datetime import datetime

##################################################################################################
#Load the data and create the plots
##################################################################################################
#Importar curvas cero cupón en pesos históricas
df_CCC_TESPESOS = pd.read_csv('D:/andrgome/Documents/BDPython/TESPESOS.csv',encoding='latin-1')
df_CCC_TESPESOS = df_CCC_TESPESOS.T #Transponer la base de datos
df_CCC_TESPESOS.index = pd.to_datetime(df_CCC_TESPESOS.index)

#Importar Datos de mercado - CDS5Y, CORP BBBUS, SWAPS IBR CP
df_BDMercado = pd.read_csv('D:/andrgome/Documents/BDPython/BDMercado.csv',encoding='latin-1')
df_SWAPS = pd.DataFrame()
df_SWAPS['CDS 5Y'] = df_BDMercado['COLOM CDS USD SR 5Y D14 Corp']/10000
df_SWAPS['CORP BBB US'] = df_BDMercado['BAMLC0A4CBBBEY']/100
df_SWAPS['IBR1Y'] = df_BDMercado['CLSWIB1 Curncy'].astype(float)
df_SWAPS['IBR2Y'] = df_BDMercado['CLSWIB2 Curncy'].astype(float)
df_SWAPS['Fecha'] = pd.to_datetime(df_BDMercado['FECHA'])
df_SWAPS.set_index('Fecha', inplace=True)
df_SWAPS['IBR1Y'] = df_SWAPS['IBR1Y']/100
df_SWAPS['IBR2Y'] = (1+df_SWAPS['IBR2Y']/400)**4-1
df_SWAPS['ZC2Y'] = ((1+df_SWAPS['IBR2Y'])/(1-df_SWAPS['IBR2Y']/(1+df_SWAPS['IBR1Y'])))**0.5-1   #Calculando tasa ZC 2Y
df_SWAPS['ZC13M'] = df_SWAPS['IBR1Y']+(df_SWAPS['IBR2Y']-df_SWAPS['IBR1Y'])*(1/12) #Interpolando tasa ZC 13 meses
df_SWAPS['FRA1M1Y'] = (((1+df_SWAPS['ZC13M'])**(13/12))/(1+df_SWAPS['IBR1Y']))**12-1 # Calculando FRA de 1mes dentro de 1Y

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

df_regresion = df_Tasas_Par2.merge(df_SWAPS, on='Fecha')
df_regresion = df_regresion[pd.to_numeric(df_regresion['IBR1Y'], errors='coerce').notnull()]

#Regresión de Ridge
X = df_regresion[['FRA1M1Y','CDS 5Y','CORP BBB US']]
y = df_regresion['PAR_TES10Y']

X_train =  X.iloc[0:2300]
X_test = X.iloc[2301:2560]
y_train= y.iloc[0:2300]
y_test = y.iloc[2301:2560]

ridge  = Ridge(alpha=1,normalize=True)
ridge.fit(X_train,y_train)
y_pred = ridge.predict(X)
MAE = median_absolute_error(y, y_pred)
banda_superior = y_pred + 2*MAE
banda_inferior = y_pred - 2*MAE

#Create the scatter plot:
Scatter_Fig=px.scatter()
Scatter_Fig.add_scatter(x=df_regresion.index, y=banda_superior,marker_size=6, marker_color='lightgrey', line_color='lightgrey',line_width=1,showlegend=False)
Scatter_Fig.add_scatter(x=df_regresion.index, y=banda_inferior,marker_size=6, marker_color='lightgrey', line_color='lightgrey',line_width=1,fill="tonexty", fillcolor='lightgrey',showlegend=False)
Scatter_Fig.add_scatter(x=df_regresion.index, y=y_pred,name='MODELO',marker_size=6, marker_color='gold', line_color='gold',line_width=1)
Scatter_Fig.add_scatter(x=df_regresion.index, y=df_regresion["PAR_TES10Y"],name='TES10Y',marker_size=6, marker_color='darkblue', line_color='darkblue',line_width=1)


Scatter_Fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
},yaxis=dict(tickformat=".2%"))


#Create Layout
tab_REG_layout = html.Div([
    html.H2("VALOR JUSTO TES", id='title'), #Creates the title of the app
#    dcc.Dropdown(id="emisor_dropdown",options=[{ 'label':l,'value':l} for l in emisor],value=['ISAGEN']),
    dcc.Graph(figure=Scatter_Fig, id='Scatter'),
    html.Div(id='page-REG-content')    
])

