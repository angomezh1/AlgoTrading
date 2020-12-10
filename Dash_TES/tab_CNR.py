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
from plotly.subplots import make_subplots
import plotly.graph_objects as go

##################################################################################################
#Load the data and create the plots
##################################################################################################
#Importar curvas cero cupón en pesos históricas
df_CCC_TES = pd.read_csv('D:/andrgome/Documents/BDPython/BD_Cheapandrich.csv',encoding='latin-1')
df_valoracion = pd.read_csv('D:/andrgome/Documents/BDPython/BDValoracion.csv',encoding='latin-1')

df_TF = df_valoracion[df_valoracion['NEMOTECNICO'].str.contains("TFIT")]   
df_TF['SPREAD VALORACIÓN'] = df_TF['SPREAD VALORACIÓN'].astype(float) #Convertir a float la columna tasa
df_TF['DÍAS AL VTO'] = df_TF['DÍAS AL VTO'].astype(float)
df_TF['AÑOS'] = df_TF['DÍAS AL VTO']/365
df_TF.sort_values(by=['AÑOS'],inplace=True)

df_UVR = df_valoracion[df_valoracion['NEMOTECNICO'].str.contains("TUVT")]   
df_UVR['SPREAD VALORACIÓN'] = df_UVR['SPREAD VALORACIÓN'].astype(float) #Convertir a float la columna tasa
df_UVR['DÍAS AL VTO'] = df_UVR['DÍAS AL VTO'].astype(float)
df_UVR['AÑOS'] = df_UVR['DÍAS AL VTO']/365
df_UVR.sort_values(by=['AÑOS'],inplace=True)

#Create the scatter plot:
fig = make_subplots(rows=1, cols=2,horizontal_spacing = 0.2)

trace1 = go.Scatter(x=df_CCC_TES["T"], y=df_CCC_TES["Fwd 1Y1Y COP"],name='FWD1Y1Y COP',marker_size=6, marker_color='dimgrey', line_color='dimgrey')
trace2 = go.Scatter(x=df_TF["AÑOS"], y=df_TF["SPREAD VALORACIÓN"],name='YTM',marker_size=6, marker_color='darkblue', line_color='gold')
trace3 = go.Scatter(x=df_CCC_TES["T"], y=df_CCC_TES["Fwd 1Y1Y UVR"],name='FWD1Y1Y UVR',marker_size=6, marker_color='gold', line_color='darkblue')
trace4 = go.Scatter(x=df_UVR["AÑOS"], y=df_UVR["SPREAD VALORACIÓN"],name='YTM',marker_size=6, marker_color='dimgrey', line_color='lightgrey')


fig.append_trace(trace1, 1, 1)# trace1 is in position 0 of the list fig['data]
fig.append_trace(trace2, 1, 1)#                       1 
fig.append_trace(trace3, 1, 2)#                       2
fig.append_trace(trace4, 1, 2)#                       3

fig['data'][1].update(yaxis='y3')
fig['data'][3].update(yaxis='y4')



fig['layout']['yaxis1'].update(                         
                         title= 'FWD1Y1Y COP',
                         )


fig['layout']['yaxis3']=dict(
                          overlaying= 'y1', 
                          anchor= 'x1', 
                          side= 'right', 
                          showgrid= False, 
                          title= 'YTM COP'
                         )

fig['layout']['yaxis2'].update(                         
                         title= 'FWD1Y1Y UVR',
                         )


fig['layout']['yaxis4']=dict(
                          overlaying= 'y2', 
                          anchor= 'x2', 
                          side= 'right', 
                          showgrid= False, 
                          title= 'YTM UVR'
                         )

fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'}
,yaxis1=dict(tickformat=".2%"),yaxis2=dict(tickformat=".2%"),yaxis3=dict(tickformat=".2%"),yaxis4=dict(tickformat=".2%"),
legend=dict(orientation="h",yanchor="bottom",y=-0.2,xanchor="right",x=0.7)
)

#Create Layout
tab_CNR_layout = html.Div([
    html.H2("ANÁLISIS RELATIVO - CHEAP AND RICH", id='title'), #Creates the title of the app
#    dcc.Dropdown(id="emisor_dropdown",options=[{ 'label':l,'value':l} for l in emisor],value=['ISAGEN']),
    dcc.Graph(figure=fig, id='Scatter'),
    html.Div(id='page-CNR-content')    
])

