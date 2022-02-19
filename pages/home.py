from app import *
from dash import html,dcc
from Backend.connector import getData
from layoutComponents.homeanalysistab import generateHTMLTable, generateOverviewTab,makeModal
from Backend.settings import BOOL
from layoutComponents.homeplotgraph import *
from layoutComponents.homeNavBar import *



config = {
    # "displayModeBar": False,
    # "showTips": False,
    "responsive":True,
    "displaylogo":False,
    "modeBarButtonsToRemove": ['zoomIn2d','autoScale2d','lasso2d','resetScale2d','zoomOut2d'],
    "modeBarButtonsToAdd":['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
    }





#Initial layout setting
stock = 'sbin'
df = getData(stock)
fig = makeGraph(df,['sma'],True)

content = offcanvascontent('',[],[])
dfs = doAnalysis(df,['macd','rsi','stoch'])
table,modalHeader = generateHTMLTable(dfs)
overview = generateOverviewTab(stock)
modal = makeModal(table,modalHeader,overview)
navbar = navLayout(content,modal)
graph = dcc.Graph(figure=fig,id='output',config=config)


layout = html.Div(children=[
                    # storeData,
                    navbar,
                    graph,
                    dcc.Link('Go to Trial', href='/trial')
                    ])