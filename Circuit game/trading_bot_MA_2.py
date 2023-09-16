import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from matplotlib.widgets import Button

BALANCE_FILE = 'balance.txt'
CAPITAL = 3000
COMMISSION = 4.95

def fetch_stock_data(ticker, start_date, end_date):
    """Fetches stock data for the given ticker and dates."""
    try:
        return yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def preprocess_data(data):
    """Computes rolling averages and Bollinger Bands needed for the strategy."""
    data['SMA10'] = data['Close'].rolling(window=10).mean()
    data['SMA45'] = data['Close'].rolling(window=45).mean()
    data['Middle Band'] = data['Close'].rolling(window=10).mean()
    data['Upper Band'] = data['Middle Band'] + 2 * data['Close'].rolling(window=20).std()
    data['Lower Band'] = data['Middle Band'] - 2 * data['Close'].rolling(window=20).std()
    data.dropna(inplace=True)
    return data

def toggle_bollinger_band_visibility(event, lines):
    """Toggle the visibility of the Bollinger Bands when a button is pressed."""
    for line in lines:
        line.set_visible(not line.get_visible())
    plt.draw()

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
            commissions += COMMISSION
            number_of_trade += 1
            
        elif position_price and not np.isnan(row['Sell_Signal']):
            selling_price = row['Close']
            selling_shares_value = selling_price * number_of_shares
            
            trade_return = selling_shares_value - invested_amount
            percentage_trade_return = ((selling_shares_value - invested_amount)/invested_amount)*100
            
            current_balance += trade_return - 5
            commissions += COMMISSION
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

def plot_stock_data(ticker, data):
    """Plots stock data with buy/sell signals and Bollinger Bands."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['Close'], label='Close Price', alpha=0.5)
    ax.scatter(data.index, data['Buy_Signal'], color='green', marker='^', label='Buy Signal', alpha=1)
    ax.scatter(data.index, data['Sell_Signal'], color='red', marker='v', label='Sell Signal', alpha=1)
    
    lines = {
        "SMA10": ax.plot(data['SMA10'], label='SMA10', alpha=0.5, color='blue')[0],
        "SMA45": ax.plot(data['SMA45'], label='SMA45', alpha=0.5, color='red')[0],
        "Middle Band": ax.plot(data['Middle Band'], label='Middle Band', alpha=0.5, color='grey')[0],
        "Upper Band": ax.plot(data['Upper Band'], label='Upper Band', alpha=0.5, color='purple')[0],
        "Lower Band": ax.plot(data['Lower Band'], label='Lower Band', alpha=0.5, color='orange')[0],
    }

    ax.set_title(f'{ticker} Close Price, Signals, and Bollinger Bands')
    ax.set_xlabel('Date')
    ax.set_ylabel(f'{ticker} Close Price')
    ax.legend(loc='upper left')

    # Button to toggle Bollinger Bands
    bollinger_bands = [lines["Middle Band"], lines["Upper Band"], lines["Lower Band"]]
    button_axes = fig.add_axes([0.8, 0.01, 0.1, 0.05])  # positioning of the button
    button = Button(button_axes, "Toggle Bollinger Bands", color='lightgoldenrodyellow', hovercolor='0.975')
    button.on_clicked(lambda event: toggle_bollinger_band_visibility(event, bollinger_bands))

    plt.show()


def main():
    ticker = input("Enter the stock ticker (e.g. AAPL): ")
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime.now()
    years = (end_date - start_date).days / 365.25  # Calculate number of years, accounting for leap years

    data = fetch_stock_data(ticker, start_date, end_date)
    data = preprocess_data(data)
    data = compute_signals(data)
    trades, commissions, number_of_trade = compute_trade_performance(data)

    end_balance = trades[-1]['Balance_After_Trade'] if trades else load_balance_from_file()  # Load end balance from file or trades
    display_trades(trades)
    
    annualized_return = calculate_annualized_return(CAPITAL, end_balance, years)
    yoy_return = calculate_yoy_return(CAPITAL, end_balance)

    print('---------------------------------------------------------------')
    print(f"Start Balance: ${CAPITAL:.2f}")
    print(f"End Balance: ${end_balance:.2f}")
    print('---------------------------------------------------------------')
    print(f"Total commissions payed: ${commissions:.2f}")
    print(f"Total number of trade: {number_of_trade:.2f}")
    print('---------------------------------------------------------------')
    print(f"Annualized Return: {annualized_return * 100:.2f}%")
    print(f"YoY Return: {yoy_return * 100:.2f}%")
    print(f"Number of years: {years}")
    print('---------------------------------------------------------------')

    plot_stock_data(ticker, data)

if __name__ == "__main__":
    main()
