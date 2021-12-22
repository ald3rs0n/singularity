#!/usr/bin/python3

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from plotly.subplots import _init_subplot_xy

from layout import *



fig = makeGraph('idea')
content = offcanvascontent('idea')

# layout =  AppLayout('iex')
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("offcanvas-scrollable", "is_open"),
    Input("open-offcanvas-scrollable", "n_clicks"),
    State("offcanvas-scrollable", "is_open"),
)
def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("offcanvas-scrollable2", "is_open"),
    Input("open-offcanvas-scrollable2", "n_clicks"),
    State("offcanvas-scrollable2", "is_open"),
)
def toggle_offcanvas_scrollable2(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    [Output('output', 'figure'),
    Output('output2','children')],
    # Output('stored-in-browser','data')
    [Input("input", "value")],
    prevent_initial_call=True
)
def output_text(value):
    # df = getFileData(value)
    fig = makeGraph(value)
    content = offcanvascontent(value)
    return fig,content
    # return df
    
# @app.callback(
#     [Output('output','figure'),
#     Output('output2','children')],
#     Input('stored-in-browser','data'),
#     prevent_initial_call = True
# )
# def output_text(data):
#     fig = makeGraph(data)
#     content = offcanvascontent(data)
#     return fig,content

navbar = makeLayout(content)
graph = dcc.Graph(figure=fig,id='output')
layout = html.Div(children=[navbar,graph])



# app = dash.Dash()
# if __name__ == '__main__':
app.layout = layout
app.run_server(debug=True)