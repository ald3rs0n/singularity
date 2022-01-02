from scipy.signal import find_peaks
from backend.dbconnect import getDataFromDB
import matplotlib.pyplot as plt

df = getDataFromDB('idea')

x = df['Close']

maxima , _ = find_peaks(x)
minima , _ = find_peaks(-1*x)

plt.plot(x)
plt.plot(maxima,x[maxima],"x")
plt.plot(minima,x[minima],"o")
plt.show()