#!/usr/bin/python3
from app import *
from Backend.settings import IP,PORT
from layoutComponents.plotgraph import *
from layoutComponents.homeNavBar import *
from layoutComponents.dccstore import *
import pages.trial as trial
import pages.home as home
import pages.dashboard as dashbd

def serve_layout():
    slayout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ])
    return slayout

app.layout = serve_layout

app.validation_layout = html.Div([
    app.layout,
    trial.layout,
    home.layout,
    dashbd.layout])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              )
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/dashboard':
        return dashbd.layout
    elif pathname == '/trial':
        return trial.layout
    else:
        return 404




if __name__ == '__main__':
    app.run_server(host=IP,port=PORT,debug=True)
    # app.run_server(host='127.0.0.1', port='7080', proxy=None, debug=False, dev_tools_ui=None, dev_tools_props_check=None, dev_tools_serve_dev_bundles=None, dev_tools_hot_reload=None, dev_tools_hot_reload_interval=None, dev_tools_hot_reload_watch_interval=None, dev_tools_hot_reload_max_retry=None, dev_tools_silence_routes_logging=None, dev_tools_prune_errors=None, **flask_run_options)
    # app.run_server()


