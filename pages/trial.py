from Backend.dbconnect import updateStockList
from Backend.getstockdata import NseStocks
from app import *
from dash import html,dcc,Output,Input,State
import pandas as pd
from Backend.connector import getData
# from Backend.dbconnect import getDataFromDBTest


content = []
content.append(dcc.Link('Go to Index', href='/'))
layout = html.Div(content)
