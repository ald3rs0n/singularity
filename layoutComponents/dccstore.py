from app import *
from dash import html,dcc,Input,Output
from dash.exceptions import PreventUpdate
from Backend.connector import getData
from Backend.settings import BOOL

storeData = html.Div([
    # dcc.Store stores the intermediate value
    dcc.Store(id='storing'),
    # html.P(id='store-output')
])

@app.callback(
    Output('storing', 'data'),
    Input("home_searchbar", "value"),
)
def store_data(stock):
    if stock is None:
        raise PreventUpdate
    df = getData(stock,BOOL)
    if df is None:
        raise PreventUpdate
    return df.to_json(date_format='iso', orient='split')
    