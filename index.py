#!/usr/bin/python3
from layout import *
from app import app
from backend.settings import IP,PORT

#Initial layout setting
df = getData('sbin')
fig = makeGraph(df,['macd'],True)
content = offcanvascontent('BANKS',['macd'])
navbar = navLayout(content)
graph = dcc.Graph(figure=fig,id='output')


index_layout = html.Div(children=[navbar,graph])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(index_layout,id='page-content')
])

# @app.callback(Output('page-content', 'children'),
#               Input('url', 'pathname'),
#               )
# def display_page(pathname):
#     if pathname == '/':
#         return app.layout
#     elif pathname == '/apps/app2':
#         pass
#         # return app2.layout
#     else:
#         return '404'




if __name__ == '__main__':
    app.run_server(host=IP,port=PORT,debug=True)
    # app.run_server(host='127.0.0.1', port='7080', proxy=None, debug=False, dev_tools_ui=None, dev_tools_props_check=None, dev_tools_serve_dev_bundles=None, dev_tools_hot_reload=None, dev_tools_hot_reload_interval=None, dev_tools_hot_reload_watch_interval=None, dev_tools_hot_reload_max_retry=None, dev_tools_silence_routes_logging=None, dev_tools_prune_errors=None, **flask_run_options)
    # app.run_server()


