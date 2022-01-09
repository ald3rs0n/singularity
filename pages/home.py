from app import *
from dash import html,dcc,Output,Input,State
import pandas as pd
from Backend.connector import getData
from layoutComponents.analysistable import generateHTMLTable,makeModal
from Backend.settings import BOOL
from layoutComponents.plotgraph import *
from layoutComponents.homeNavBar import *
from layoutComponents.dccstore import *
# from validation import *

#Initial layout setting
df = getData('sbin',BOOL)
fig = makeGraph(df,['macd'],True)

content = offcanvascontent('',[],on=BOOL)
dfs = doAnalysis(df,['macd','rsi','stoch'])
table = generateHTMLTable(dfs)
modal = makeModal(table)
navbar = navLayout(content,modal)
graph = dcc.Graph(figure=fig,id='output')


layout = html.Div(children=[
                    navbar,
                    graph,
                    storeData,
                    dcc.Link('Go to Index', href='/trial')
                    ])