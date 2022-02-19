from Backend.settings import BOOL
from layoutComponents.homeplotgraph import *
from layoutComponents.dashbdLayout import *
# from layoutComponents.dccstore import *

def dashboardlayout():
    navBar = dashbdNavLayout()
    dashboardBody = dashbdBodyLayout()
    layout = html.Div(children=[
                        navBar,
                        dashboardBody,
                        dcc.Link('Go to Index', href='/trial')
                        ])
    return layout


