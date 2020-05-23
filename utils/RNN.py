import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

from utils.helper import plotPlaces

def getPlaceSerie(df, place, agg_factor, dataset):
    _, df_inc = plotPlaces(df, np.array([place]), agg_factor=agg_factor, dataset=dataset, plot=False)
    serie = df_inc['Contagios diarios'].to_numpy()
    return serie
class RNN:

    def __init__(self, data, window_size=7, lstm_units=16, epochs=150):
        serie = data.reshape(data.shape[0], 1)

        self.window_size = window_size
        self.epochs = epochs

        # normalize the dataset
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.serie_scaled = serie_scaled = self.scaler.fit_transform(serie)

        _, self.X, self.y = self.__getRNNDataset__(self.serie_scaled, window_size)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        self.X_train = np.reshape(self.X_train, (self.X_train.shape[0], 1, self.X_train.shape[1]))
        self.X_test = np.reshape(self.X_test, (self.X_test.shape[0], 1, self.X_test.shape[1]))

        # Define Model
        self.model = Sequential()
        self.model.add(LSTM(lstm_units, input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def train(self, verbose=0):
        history = self.model.fit(self.X_train, self.y_train, epochs=self.epochs, batch_size=1, validation_data=(self.X_test, self.y_test), verbose=verbose, shuffle=False)
        score = self.model.evaluate(self.X_test, self.y_test, batch_size=4)
        return history, score

    def getAllPredictions(self, verbose=0):
        y_pred = self.model.predict(np.reshape(self.X, (self.X.shape[0], 1, self.X.shape[1])), batch_size=1, verbose=verbose)
        return self.scaler.inverse_transform(self.y), self.scaler.inverse_transform(y_pred)

    def predict(self, num_samples, verbose=0):
        predictions = []
        last_samples = self.serie_scaled[-self.window_size:].T
        for i in np.arange(num_samples):
            prediction = self.model.predict(np.reshape(last_samples, (last_samples.shape[0], 1, last_samples.shape[1])), batch_size=1, verbose=verbose)[0][0]
            predictions.append(prediction)
            list = last_samples.tolist()[0]
            list.append(prediction)
            last_samples = np.array(list)[-self.window_size:].reshape(1, self.window_size)
        return self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    def __getRNNDataset__(self, serie, group_size):
        df_serie = pd.DataFrame()
        l = len(serie)
        index = group_size + 1
        while (index <= l):
            line = serie[index - group_size - 1:index].T[0]
            index = index + 1
            # print('line : ',line)
            df_serie = pd.concat(objs=[df_serie, pd.DataFrame([line])], axis=0, ignore_index=True)
        X = df_serie.drop(labels=[group_size], axis=1).to_numpy()
        y = df_serie[[group_size]].to_numpy()
        return df_serie, X, y

