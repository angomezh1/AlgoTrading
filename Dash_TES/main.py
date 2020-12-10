import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from tabs import tab_BEI
from tabs import tab_ASW
from tabs import tab_REG
from tabs import tab_CNR

app = dash.Dash()

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.H1('Tablero TES'),
    dcc.Tabs(id="tabs-TES", value='tab-BEI', children=[
        dcc.Tab(label='Break Even Inflation', value='tab-BEI'),
        dcc.Tab(label='Asset Swap Spread', value='tab-ASW'),
        dcc.Tab(label='Valor Justo TES', value='tab-REG'),
        dcc.Tab(label='Cheap and Rich', value='tab-CNR'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs-TES', 'value')])
def render_content(tab):
    if tab == 'tab-BEI':
        return tab_BEI.tab_BEI_layout
    elif tab == 'tab-ASW':
        return tab_ASW.tab_ASW_layout
    elif tab == 'tab-REG':
        return tab_REG.tab_REG_layout
    elif tab == 'tab-CNR':
        return tab_CNR.tab_CNR_layout


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)