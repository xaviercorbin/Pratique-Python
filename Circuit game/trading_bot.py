import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import matplotlib.pyplot as plt

CAPITAL = 1000  # Capital de départ en USD
RISK_PER_TRADE = 0.05  # Risquer 1% du capital par trade
STOP_LOSS = 0.02  # 2% de perte avant de sortir
TAKE_PROFIT = 0.05  # Prendre le profit après 5% de gain

# Ajouter la fonction de gestion des risques pour déterminer la taille de la position
def position_size(price, capital=CAPITAL, risk=RISK_PER_TRADE):
    return (capital * risk) / price

# Télécharger les données depuis Yahoo Finance
def get_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Calculer le RSI
def RSI(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
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

# Stratégie de trading avec gestion des risques
def trading_strategy_risk_managed(data):
    buy_signals = []
    sell_signals = []
    stop_loss_levels = []
    take_profit_levels = []

    position = None
    for i in range(len(data)):
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
        elif data['SMA10'].iloc[i] > data['SMA45'].iloc[i] and data['RSI'].iloc[i] < 30:
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

    return buy_signals, sell_signals, stop_loss_levels, take_profit_levels


# Obtenir les données
ticker = input("Enter the stock ticker (e.g. AAPL): ")
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime.now()
data = get_data(ticker, start_date, end_date)

# Calculer les moyennes mobiles
data['SMA10'] = data['Close'].rolling(window=10).mean()
data['SMA45'] = data['Close'].rolling(window=45).mean()

# Calculer RSI
data = RSI(data, window=14)

# Générer les signaux d'achat et de vente avec gestion des risques
data['Buy_Signal'], data['Sell_Signal'], data['Stop_Loss'], data['Take_Profit'] = trading_strategy_risk_managed(data)

# Compute the trade results AFTER the signals are generated
data['Trade_Results'] = compute_trade_results(data)

# Plotting
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
plt.show()

# Modify pandas display options to show all rows
pd.set_option('display.max_rows', None)

print(data)

print(data.tail())