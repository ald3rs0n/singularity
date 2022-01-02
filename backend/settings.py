import socket
import dash_daq as daq
import pandas as pd

#Network handlling part: IP and PORT
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    # doesn't even have to be reachable
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
except Exception:
    IP = '127.0.0.1'
finally:
    s.close()
PORT = 7000

# daq theme settings
theme = {
    'dark' : True
    }
daq.DarkThemeProvider(theme=theme)

#stock dataframe from csv
STDF = pd.read_csv('static/stocks.csv')


