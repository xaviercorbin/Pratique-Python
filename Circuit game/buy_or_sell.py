import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import FigureCanvasTkAgg
from tabulate import tabulate

BALANCE_FILE = 'balance.txt'
CAPITAL = 3000

# Initialize global variables for navigation through graphs
current_stock_index = 0
stocks_data = []
table_data = []

def fetch_stock_data(ticker, start_date, end_date):
    """Fetches stock data for the given ticker and dates."""
    try:
        return yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def preprocess_data(data):
    """Computes rolling averages needed for the strategy."""
    data['SMA10'] = data['Close'].rolling(window=10).mean()
    data['SMA45'] = data['Close'].rolling(window=45).mean()
    data.dropna(inplace=True)
    return data

def compute_signals(data):
    """Computes buy and sell signals based on moving average crossover."""
    data['Buy_Signal'] = np.where(
        (data['SMA10'] > data['SMA45']) & (data['SMA10'].shift(1) <= data['SMA45'].shift(1)), 
        data['Close'], np.nan)

    data['Sell_Signal'] = np.where(
        (data['SMA10'] < data['SMA45']) & (data['SMA10'].shift(1) >= data['SMA45'].shift(1)), 
        data['Close'], np.nan)

    return data

def save_balance_to_file(balance):
    """Saves the balance to a txt file."""
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(CAPITAL)) # for the moment its capital

def load_balance_from_file():
    """Loads the balance from a txt file. If not found, returns the initial CAPITAL."""
    try:
        with open(BALANCE_FILE, 'r') as f:
            return float(f.read().strip())
    except FileNotFoundError:
        return CAPITAL

def calculate_annualized_return(start_balance, end_balance, years):
    if years == 0:  # Prevent division by zero
        return 0
    return (end_balance / start_balance) ** (1 / years) - 1

def calculate_yoy_return(start_balance, end_balance):
    return (end_balance - start_balance) / start_balance

def get_latest_signal(ticker, data):
    """Returns the latest signal (Buy, Sell, or None) for the provided stock data."""
    #print("Buy Signal for last row:", data['Buy_Signal'].iloc[-1])
    #print("Sell Signal for last row:", data['Sell_Signal'].iloc[-1])
    
    if data['Buy_Signal'].iloc[-1] > 0:
        return "Buy"
    elif data['Sell_Signal'].iloc[-1] > 0:
        return "Sell"
    else:
        return None

def compute_trade_performance(data):
    """Computes trade performance for the given data."""
    trades = []
    current_balance = load_balance_from_file()  # Load balance from file
    position_price = None
    shares = 0
    commissions = 0
    number_of_trade = 0

    for i, row in data.iterrows():
        if not position_price and not np.isnan(row['Buy_Signal']):
            position_price = row['Close']
            
            pre_number_of_shares = current_balance / position_price
            number_of_shares = round(pre_number_of_shares)-1
            
            invested_amount = position_price * number_of_shares
            current_balance -= 5
            commissions += 5
            number_of_trade += 1
            
        elif position_price and not np.isnan(row['Sell_Signal']):
            selling_price = row['Close']
            selling_shares_value = selling_price * number_of_shares
            
            trade_return = selling_shares_value - invested_amount
            percentage_trade_return = ((selling_shares_value - invested_amount)/invested_amount)*100
            
            current_balance += trade_return - 5
            commissions += 5
            number_of_trade += 1
            save_balance_to_file(current_balance)  # Save updated balance to file

            trades.append({
                'Buy_Date': i - pd.Timedelta(days=1),
                'Buy_Price': position_price,
                'Sell_Date': i,
                'Sell_Price': selling_price,
                'Shares': number_of_shares,
                'Invested_Amount': invested_amount,
                'Trade_Return': trade_return,
                '% Change': percentage_trade_return,
                'Balance_After_Trade': current_balance
            })
            
            
            position_price = None
            invested_amount = None
            trade_return = None
            selling_price = None
            selling_shares_value = None
            percentage_trade_return = None
            number_of_shares = None


    return trades, commissions, number_of_trade


def display_trades(trades):
    """Prints out trade details."""
    for trade in trades:
        print(f"Trade: [Buy Date: {trade['Buy_Date']}, Buy Price: ${trade['Buy_Price']:.2f}, "
              f"Sell Date: {trade['Sell_Date']}, Sell Price: ${trade['Sell_Price']:.2f}, "
              f"Shares: {trade['Shares']}]-> Trade Return: ${trade['Trade_Return']:.2f} -> "
              f"Balance After Trade: ${trade['Balance_After_Trade']:.2f}\n")

def plot_stock_data(ticker, data, canvas=None):
    """Plots stock data with buy/sell signals."""
    if canvas:  # If canvas is provided, clear the current figure
        plt.figure(canvas.figure.number)  # This line was changed
    else:  # Otherwise, create a new figure
        plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.scatter(data.index, data['Buy_Signal'], color='green', marker='^', label='Buy Signal', alpha=1)
    plt.scatter(data.index, data['Sell_Signal'], color='red', marker='v', label='Sell Signal', alpha=1)
    plt.plot(data['SMA10'], label='SMA10', alpha=0.5, color='blue')
    plt.plot(data['SMA45'], label='SMA45', alpha=0.5, color='red')
    plt.title(f'{ticker} Close Price and Signals')
    plt.xlabel('Date')
    plt.ylabel(f'{ticker} Close Price')
    plt.legend(loc='best')
    if canvas:
        canvas.draw()
    else:
        plt.show()


def next_stock(canvas):
    global current_stock_index
    current_stock_index = (current_stock_index + 1) % len(stocks_data)
    ticker, data, _ = stocks_data[current_stock_index]
    plot_stock_data(ticker, data, canvas)

def prev_stock(canvas):
    global current_stock_index
    current_stock_index = (current_stock_index - 1) % len(stocks_data)
    ticker, data, _ = stocks_data[current_stock_index]
    plot_stock_data(ticker, data, canvas)



def main():
    tickers = input("Enter the stock tickers separated by commas (e.g. AAPL,MSFT,GOOGL): ").split(",")
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime.now()

    stocks_to_buy = []
    stocks_to_sell = []
    
    global stocks_data, table_data

    for ticker in tickers:
        ticker = ticker.strip()
        data = fetch_stock_data(ticker, start_date, end_date)
        if data is None:
            continue
        data = preprocess_data(data)
        data = compute_signals(data)
        latest_signal = get_latest_signal(ticker, data)

        trades, _, _ = compute_trade_performance(data)
        stocks_data.append((ticker, data, trades))

        if latest_signal == "Buy":
            stocks_to_buy.append(ticker)
        elif latest_signal == "Sell":
            stocks_to_sell.append(ticker)

    # Create the main GUI window
    root = Tk()
    root.title("Stock Analysis")

    # Create navigation buttons
    prev_button = Button(root, text="Previous", command=lambda: prev_stock(canvas))
    prev_button.pack(side=LEFT)

    next_button = Button(root, text="Next", command=lambda: next_stock(canvas))
    next_button.pack(side=RIGHT)

    # Create a canvas for displaying graphs
    canvas = FigureCanvasTkAgg(plt.figure(figsize=(12, 6)), master=root)
    canvas.get_tk_widget().pack()

    # Initial plot
    ticker, data, _ = stocks_data[current_stock_index]
    plot_stock_data(ticker, data, canvas)

    # Display stock table in the terminal
    table_data = []
    for ticker, data, trades in stocks_data:
        latest_signal = get_latest_signal(ticker, data)
        table_data.append([ticker, data['Close'][-1], len(trades), latest_signal])

    table_headers = ["Ticker", "Price", "Number of Shares", "Signal"]
    print(tabulate(table_data, headers=table_headers, tablefmt="pretty"))

    root.mainloop()

if __name__ == "__main__":
    main()