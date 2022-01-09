from Backend.settings import BOOL
from layoutComponents.plotgraph import *
from layoutComponents.dashbdLayout import *
from layoutComponents.dccstore import *
# from validation import *


#Initial layout setting
df = getData('sbin',BOOL)
# content = offcanvascontent('BANKS',['macd'],on=False)
navBar = dashbdNavLayout()
dashboardBody = dashbdBodyLayout()

layout = html.Div(children=[
                    navBar,
                    dashboardBody,
                    storeData,
                    dcc.Link('Go to Index', href='/trial')
                    ])



