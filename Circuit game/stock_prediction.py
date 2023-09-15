import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

def split_data(X, y, train_size):
    split = int(train_size * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    return X_train, X_test, y_train, y_test

def create_lstm_model(look_back):
    model = Sequential()
    model.add(LSTM(50, input_shape=(look_back, 1), return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, X_train, y_train, epochs, batch_size):
    from tensorflow.keras.callbacks import EarlyStopping
    early_stop = EarlyStopping(monitor='val_loss', patience=10)
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_split=0.2, callbacks=[early_stop])
    return model, history

def plot_predictions(y_test_inv, predictions, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(y_test_inv, color='blue', label='Actual Stock Price')
    plt.plot(predictions, color='red', label='Predicted Stock Price')
    plt.title(f'{ticker} Stock Price Prediction using LSTM')
    plt.xlabel('Days')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

def main():
    ticker = input("Enter the stock ticker (e.g. AAPL): ")
    stock_data = fetch_stock_data(ticker, start="2010-01-01", end="2023-01-01")
    look_back = 15  
    X, y, scaler = preprocess_data(stock_data, look_back)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    X_train, X_test, y_train, y_test = split_data(X, y, 0.8)

    model = create_lstm_model(look_back)
    model, history = train_model(model, X_train, y_train, epochs=50, batch_size=1)

    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions.reshape(-1, 1))
    y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))

    mse = mean_squared_error(y_test_inv, predictions)
    print(f"Mean Squared Error: {mse}")
    plot_predictions(y_test_inv, predictions, ticker)

if __name__ == "__main__":
    main()
