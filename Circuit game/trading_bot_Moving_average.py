import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA

# Constants
CAPITAL = 100
RISK_PER_TRADE = 0.8
STOP_LOSS = 0.01
TAKE_PROFIT = 0.05

# Helper Functions
def position_size(price, capital=CAPITAL, risk=RISK_PER_TRADE):
    return (capital * risk) / price

def is_valid_ticker(ticker_symbol):
    try:
        yf.Ticker(ticker_symbol)
        return True
    except:
        return False

def get_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def RSI(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    with np.errstate(divide='ignore', invalid='ignore'):
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
    rsi[avg_loss == 0] = 100 if avg_gain.iloc[0] != 0 else 0
    data['RSI'] = rsi
    return data


def compute_trade_results(data):
    results = [np.nan] * len(data)
    position = None
    for i in range(1, len(data)):
        if not position and not np.isnan(data['Buy_Signal'].iloc[i]):
            position = data['Close'].iloc[i]
        elif position and not np.isnan(data['Sell_Signal'].iloc[i]):
            results[i] = (data['Close'].iloc[i] - position) / position
            position = None
    return results

def trading_strategy_risk_managed(data, model):
    buy_signals = []
    sell_signals = []
    stop_loss_levels = []
    take_profit_levels = []

    position = None

    for i in range(len(data)-1):
        # Using the model to predict the next day's closing price
        try:
            next_close_prediction = model.predict(start=len(data)-len(data)+i, end=len(data)-len(data)+i)[0]
        except:
            next_close_prediction = None

        if position:
            if data['Close'].iloc[i] <= position['stop_loss'] or data['Close'].iloc[i] >= position['take_profit']:
                sell_signals.append(data['Close'].iloc[i])
                buy_signals.append(np.nan)
                position = None
            else:
                buy_signals.append(np.nan)
                sell_signals.append(np.nan)
            stop_loss_levels.append(np.nan)
            take_profit_levels.append(np.nan)
        elif next_close_prediction and next_close_prediction > data['Close'].iloc[i] and data['RSI'].iloc[i] < 30:
            size = position_size(data['Close'].iloc[i])
            position = {
                'price': data['Close'].iloc[i],
                'size': size,
                'stop_loss': data['Close'].iloc[i] - (STOP_LOSS * data['Close'].iloc[i]),
                'take_profit': data['Close'].iloc[i] + (TAKE_PROFIT * data['Close'].iloc[i])
            }
            buy_signals.append(data['Close'].iloc[i])
            sell_signals.append(np.nan)
            stop_loss_levels.append(position['stop_loss'])
            take_profit_levels.append(position['take_profit'])
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)
            stop_loss_levels.append(np.nan)
            take_profit_levels.append(np.nan)
    else:
        buy_signals.append(np.nan)
        sell_signals.append(np.nan)
        stop_loss_levels.append(np.nan)
        take_profit_levels.append(np.nan)

    return buy_signals, sell_signals, stop_loss_levels, take_profit_levels


def fit_arima_model(y_train):
    model = ARIMA(y_train, order=(5,1,0))
    model_fit = model.fit()
    return model_fit


def prompt_for_ticker():
    while True:
        ticker = input("Enter the stock ticker (e.g. AAPL): ")
        if is_valid_ticker(ticker):
            return ticker
        else:
            print("Invalid ticker symbol. Please try again.")

def preprocess_data(data):
    data['SMA10'] = data['Close'].rolling(window=10).mean()
    data['SMA45'] = data['Close'].rolling(window=45).mean()
    data = RSI(data, window=14)
    data['Prev_Close1'] = data['Close'].shift(1)
    data['Prev_Close2'] = data['Close'].shift(2)
    data['Prev_Volume1'] = data['Volume'].shift(1)
    data.dropna(inplace=True)
    return data

def plot_data(ticker, data):
    # Convert Period index to datetime
    data.index = data.index.to_timestamp()

    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.scatter(data.index, data['Buy_Signal'], color='green', marker='^', label='Buy Signal', alpha=1)
    plt.scatter(data.index, data['Sell_Signal'], color='red', marker='v', label='Sell Signal', alpha=1)
    plt.scatter(data.index, data['Stop_Loss'], color='orange', marker='x', label='Stop Loss', alpha=1)
    plt.scatter(data.index, data['Take_Profit'], color='blue', marker='x', label='Take Profit', alpha=1)
    plt.title(f'{ticker} Close Price and Signals')
    plt.xlabel('Date')
    plt.ylabel(f'{ticker} Close Price')
    plt.legend(loc='best')
    
    # plot moving average
    plt.plot(data['SMA10'], label='SMA10', alpha=0.5, color='blue')
    plt.plot(data['SMA45'], label='SMA45', alpha=0.5, color='red')
    


def main():
    ticker = prompt_for_ticker()

    start_date = datetime.datetime(2012, 1, 1)
    end_date = datetime.datetime.now()
    data = get_data(ticker, start_date, end_date)
    data.index = pd.DatetimeIndex(data.index).to_period('D')  # Setting frequency to daily

    data = preprocess_data(data)
    features = ['Prev_Close1', 'Prev_Close2', 'Prev_Volume1', 'SMA10', 'SMA45', 'RSI']
    X = data[features]
    y = data['Close'].loc[X.index]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = fit_arima_model(y_train)
    forecast = model.forecast(steps=len(X_test))
    mse = mean_squared_error(y_test, forecast)
    print(f"Mean Squared Error of Predictions: {mse}")

    data['Buy_Signal'], data['Sell_Signal'], data['Stop_Loss'], data['Take_Profit'] = trading_strategy_risk_managed(data, model)
    data['Trade_Results'] = compute_trade_results(data)
    plot_data(ticker, data)

    pd.set_option('display.max_rows', None)
    
    start_balance = CAPITAL
    trade_results = data['Trade_Results'].dropna()
    end_balance = start_balance + start_balance * trade_results.sum()

    #print(data)
    #print(data.tail())
    
    print(f"Start Balance: ${start_balance:.2f}")
    print(f"End Balance: ${end_balance:.2f}")
    plt.show()

if __name__ == "__main__":
    main()