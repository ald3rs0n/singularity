#!/usr/bin/python3
from layout import *
from app import app

df = getFileData('sbin')
fig = makeGraph(df,['macd'])
content = offcanvascontent(df,['macd'])
navbar = navLayout(content)
graph = dcc.Graph(figure=fig,id='output')


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])


# @app.callback(Output('page-content', 'children'),
#               Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == '/apps/app1':
#         return app.layout
#     elif pathname == '/apps/app2':
#         pass
#         # return app2.layout
#     else:
#         return '404'


index_layout = html.Div(children=[navbar,graph])

app.layout = index_layout

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server()


