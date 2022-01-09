# from Backend import dbconnect as dc
from singularity.Backend.dbconnect import getDataFromDB

df = getDataFromDB('Sbin')
print(df)