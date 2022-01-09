from app import *
from dash import html,dcc,Output,Input,State
import pandas as pd
from Backend.connector import getData
# from Backend.dbconnect import getDataFromDBTest


# df = getDataFromDBTest("ONGC")

content = []
# for i,v in df.iterrows():
#     para = html.P(v)
#     content.append(para)

content.append(dcc.Link('Go to Index', href='/'))
layout = html.Div(content)
