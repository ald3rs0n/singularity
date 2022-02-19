from cProfile import label
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM,Dense,Dropout


from Backend.dbconnect import getDataFromDB


dataset_train = getDataFromDB("SBIN")
training_set = dataset_train.iloc[:,4:5].values

scaler = MinMaxScaler(feature_range=(0,1))
scaled_training_set = scaler.fit_transform(training_set)

X_train = []
Y_train = []

for i in range(60,262):
    X_train.append(scaled_training_set[i-60:i,0])
    Y_train.append(scaled_training_set[i,0])


X_train = np.array(X_train)
Y_train = np.array(Y_train)

X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1))

regressor = Sequential()
regressor.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1],1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units=1))

regressor.compile(optimizer='adam',loss='mean_squared_error')
regressor.fit(X_train,Y_train,epochs=100,batch_size=32)



dataset_test = getDataFromDB("SBIN")
actual_stock_price = dataset_test.iloc[:,4:5].values

dataset_total = pd.concat((dataset_train['Open'],dataset_test['Open']),axis=0)
inputs = dataset_total[len(dataset_total)-len(dataset_test)-60:].values

inputs = inputs.reshape(-1,1)
inputs = scaler.transform(inputs)

X_test = []
for i in range(60,80):
    X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

plt.plot(actual_stock_price,color='red',label='actual stock price')
plt.plot(predicted_stock_price,color='blue',label='predicted stock price')
plt.legend()
plt.show()



# print(actual_stock_price)
# print(X_train.shape)

# print(training_set)
# print(scaled_training_set)
