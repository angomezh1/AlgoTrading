import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import numpy as np


##################################################################################################
#Load the data and create the plots
##################################################################################################
df_CCC_TESPESOS = pd.read_csv('D:/andrgome/Documents/BDPython/TESPESOS.csv',encoding='latin-1')
df_CCC_TESPESOS = df_CCC_TESPESOS.T #Transponer la base de datos
df_CCC_TESUVR = pd.read_csv('D:/andrgome/Documents/BDPython/TESUVR.csv',encoding='latin-1')
df_CCC_TESUVR = df_CCC_TESUVR.T #Transponer la base de datos

df_CCC_TESPESOS.index = pd.to_datetime(df_CCC_TESPESOS.index)
df_CCC_TESUVR.index = pd.to_datetime(df_CCC_TESUVR.index)

df_BEI = pd.DataFrame()
df_BEI['2Y'] = (1+df_CCC_TESPESOS[730]/100)/(1+df_CCC_TESUVR[730]/100) - 1
df_BEI['5Y'] = (1+df_CCC_TESPESOS[5*365]/100)/(1+df_CCC_TESUVR[5*365]/100) - 1
df_BEI['10Y'] = (1+df_CCC_TESPESOS[10*365]/100)/(1+df_CCC_TESUVR[10*365]/100) - 1
df_BEI['15Y'] = (1+df_CCC_TESPESOS[15*365]/100)/(1+df_CCC_TESUVR[15*365]/100) - 1
df_BEI['30Y'] = (1+df_CCC_TESPESOS[30*365]/100)/(1+df_CCC_TESUVR[30*365]/100) - 1

#Create the scatter plot:
Scatter_Fig=px.scatter()
Scatter_Fig.add_scatter(x=df_BEI.index, y=df_BEI["2Y"],name='2Y',marker_size=6, marker_color='dimgrey', line_color='dimgrey',line_width=1)
Scatter_Fig.add_scatter(x=df_BEI.index, y=df_BEI["5Y"],name='5Y',marker_size=6, marker_color='gold', line_color='gold',line_width=1)
Scatter_Fig.add_scatter(x=df_BEI.index, y=df_BEI["10Y"],name='10Y',marker_size=6, marker_color='darkblue', line_color='darkblue',line_width=1)
Scatter_Fig.add_scatter(x=df_BEI.index, y=df_BEI["15Y"],name='15Y',marker_size=6, marker_color='lightgrey', line_color='lightgrey',line_width=1)
Scatter_Fig.add_scatter(x=df_BEI.index, y=df_BEI["30Y"],name='30Y',marker_size=6, marker_color='plum', line_color='plum',line_width=1)

Scatter_Fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
},yaxis=dict(tickformat=".2%"))


#Create Layout
tab_BEI_layout = html.Div([
    html.H2("BREAK EVEN INFLATION TES", id='title'), #Creates the title of the app
#    dcc.Dropdown(id="emisor_dropdown",options=[{ 'label':l,'value':l} for l in emisor],value=['ISAGEN']),
    dcc.Graph(figure=Scatter_Fig, id='Scatter'),
    html.Div(id='page-BEI-content')    
])

