from cmath import inf
from app import *
from dash import html,dcc
from Backend.stock import Stock
from layoutComponents.homeNavBar import *
from layoutComponents.homeplotgraph import *
from layoutComponents.homeanalysistab import *



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
this = Stock(stock)
df = this.df
fig = makeGraph(df,['sma'],True)
content = offcanvascontent('',[],[])
# dfs = doAnalysis(df,['macd','rsi','stoch'])
modalHeader,table,overview,info,details = generateTabs(stock)
# info,details = generateInfoTab(this)
# overview = generateOverviewTab(stock)
# overview = generateOverviewTab(this)
# table,modalHeader = generateHTMLTable(this)
modal = makeModal(table,modalHeader,overview,info,details)
navbar = navLayout(content,modal)
graph = dcc.Graph(figure=fig,id='output',config=config)


layout = html.Div(children=[
                    # storeData,
                    navbar,
                    graph,
                    dcc.Link('Go to Trial', href='/trial')
                    ])