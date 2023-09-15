import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

def fetch_stock_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data[['Close']]

def preprocess_data(stock_data, look_back):
    data = stock_data.values.reshape(-1, 1)
    scaler = MinMaxScaler()
    data = scaler.fit_transform(data)
    
    X, y = [], []
    for i in range(look_back, len(data) - 1):
        X.append(data[i - look_back:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y), scaler

def create_lstm_model(look_back):
    model = Sequential()
    model.add(LSTM(50, input_shape=(look_back, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def main():
    ticker = input("Enter the stock ticker (e.g. AAPL): ")
    stock_data = fetch_stock_data(ticker, start="2010-01-01", end="2023-01-01")

    look_back = 15  # How many past days the model will look at to predict the next day
    X, y, scaler = preprocess_data(stock_data, look_back)

    # Reshape to [samples, time steps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Splitting data into training and testing sets
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = create_lstm_model(look_back)
    model.fit(X_train, y_train, epochs=50, batch_size=1, verbose=1)

    predictions = model.predict(X_test)

    # Reverse the MinMaxScaler transformation to get actual prices
    predictions = scaler.inverse_transform(predictions.reshape(-1, 1))
    y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))

    mse = mean_squared_error(y_test_inv, predictions)
    print(f"Mean Squared Error: {mse}")

    plt.figure(figsize=(12, 6))
    plt.plot(y_test_inv, color='blue', label='Actual Stock Price')
    plt.plot(predictions, color='red', label='Predicted Stock Price')
    plt.title(f'{ticker} Stock Price Prediction using LSTM')
    plt.xlabel('Days')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
