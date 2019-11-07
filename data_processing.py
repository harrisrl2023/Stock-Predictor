from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import EarlyStopping

# This python file will process the data and train it.
# No prediction will be done in here

df = pd.read_csv('tesla.csv')  # TODO make so user can choose csv
df = df.set_index(df['Date'])
most_recent = pd.Timestamp(df['Date'].max())
trainingRange = str(most_recent - dt.timedelta(days=20))
train = df.loc[:trainingRange, ['Adj Close']]
test = df.loc[trainingRange:, ['Adj Close']]
scaler = MinMaxScaler(feature_range=(0, 1))  # set values between 0 and 1
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)


def to_sequences(seq_size, obs):
    x = []
    y = []

    for i in range(len(obs) - seq_size - 1):
        window = obs[i:(i + seq_size)]
        x.append(window)
        y.append(obs[i+seq_size])
    return np.array(x), np.array(y)


X_train, Y_train = to_sequences(5, train_scaled)
X_test, Y_test = to_sequences(5, test_scaled)
print(X_test)
X_train = np.reshape(X_train,(X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

print(X_train.shape, Y_train.shape)
model = Sequential()
model.add(LSTM(12, input_shape=(X_train.shape[1], 1), activation='relu'))
model.add(Dropout(.2))
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
monitor = EarlyStopping(monitor='loss', min_delta=1e-3, patience=10,
                        verbose=1, mode='auto', restore_best_weights=True)


model.fit(X_train, Y_train, validation_data=(X_test, Y_test),
          callbacks=[monitor], verbose=1, epochs=200)

# TODO Move code for predictions somewhere else
prediction = model.predict(X_test)
plt.plot(Y_test)
plt.plot(prediction)
plt.show()
