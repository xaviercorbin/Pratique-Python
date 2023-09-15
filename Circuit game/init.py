import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data

def add_features(stock_data):
    # Add a simple moving average
    stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA200'] = stock_data['Close'].rolling(window=200).mean()
    stock_data.dropna(inplace=True)  # remove rows with NaN values
    return stock_data

def preprocess_data(stock_data):
    stock_data['Prediction'] = stock_data['Close'].shift(-1)
    stock_data.dropna(inplace=True)

    # Using more features for prediction
    X = stock_data[['Open', 'High', 'Low', 'Close', 'SMA50', 'SMA200']].values
    y = stock_data['Prediction'].values

    # Normalize data
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    return train_test_split(X, y, test_size=0.2), scaler

def predict_stock(X_train, X_test, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred

def main():
    ticker = input("Enter the stock ticker (e.g. AAPL): ")
    stock_data = fetch_stock_data(ticker, start="2020-01-01", end="2023-01-01")

    stock_data = add_features(stock_data)
    (X_train, X_test, y_train, y_test), scaler = preprocess_data(stock_data)

    predictions = predict_stock(X_train, X_test, y_train)

    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    plt.figure(figsize=(12, 6))
    plt.plot(y_test, color='blue', label='Actual Stock Price')
    plt.plot(predictions, color='red', label='Predicted Stock Price')
    plt.title(f'{ticker} Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
