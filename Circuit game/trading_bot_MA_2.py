import datetime
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from config import date_start
from fetch_market_return import \
    compute_daily_returns as compute_market_daily_returns
from fetch_market_return import fetch_market_data, market_annualized_return
from matplotlib.widgets import Button

# Constants
BALANCE_FILE = 'balance.txt'
CAPITAL = 1000.0
COMMISSION = 4.95
BETA = 1
RISKFREERATE = 0.0531
TRADING_DAYS = 252


# ADD THE MACD TO HAVE A BETTER PREDICTION ON THE PRICE MOVEMENTS MACD(12,26,9)


def fetch_stock_data(ticker: str, start_date: datetime.datetime, end_date: datetime.datetime) -> Optional[pd.DataFrame]:
    """Fetches stock data for the given ticker and dates."""
    try:
        return yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """Computes rolling averages and Bollinger Bands needed for the strategy."""
    data['SMA10'] = data['Close'].rolling(window=10).mean()
    data['SMA45'] = data['Close'].rolling(window=45).mean()
    data['Middle Band'] = data['SMA10']
    data['Upper Band'] = data['Middle Band'] + \
        2 * data['Close'].rolling(window=20).std()
    data['Lower Band'] = data['Middle Band'] - \
        2 * data['Close'].rolling(window=20).std()
    data.dropna(inplace=True)
    return data


def compute_daily_returns(data: pd.DataFrame) -> pd.DataFrame:
    """Computes daily returns based on close prices."""
    data['Daily_Returns'] = data['Close'].pct_change()
    return data


def compute_beta_stock(stock_returns: pd.Series, market_returns: pd.Series) -> float:
    covariance = stock_returns.cov(market_returns)
    variance = market_returns.var()
    beta_stock = covariance / variance
    return beta_stock


def save_balance_to_file(balance: float) -> None:
    """Saves the balance to a txt file."""
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))


def load_balance_from_file() -> float:
    """Loads the balance from a txt file. If not found, returns the initial CAPITAL."""
    try:
        with open(BALANCE_FILE, 'r') as f:
            return float(f.read().strip())
    except FileNotFoundError:
        return CAPITAL


def compute_signals(data: pd.DataFrame) -> pd.DataFrame:
    """Computes buy and sell signals based on moving average crossover."""
    buy_conditions = (data['SMA10'] > data['SMA45']) & (
        data['SMA10'].shift(1) <= data['SMA45'].shift(1))
    sell_conditions = (data['SMA10'] < data['SMA45']) & (
        data['SMA10'].shift(1) >= data['SMA45'].shift(1))

    data['Buy_Signal'] = np.where(buy_conditions, data['Close'], np.nan)
    data['Sell_Signal'] = np.where(sell_conditions, data['Close'], np.nan)

    return data


def toggle_visibility(event, lines: List[plt.Line2D]) -> None:
    """Toggle the visibility of the lines when a button is pressed."""
    for line in lines:
        line.set_visible(not line.get_visible())
    plt.draw()


def calculate_annualized_return(start_balance: float, end_balance: float, years: float) -> float:
    return 0 if years == 0 else (end_balance / start_balance) ** (1 / years) - 1


def calculate_yoy_return(start_balance: float, end_balance: float) -> float:
    return (end_balance - start_balance) / start_balance


def compute_trade_performance(data: pd.DataFrame) -> Tuple[List[Dict[str, Union[datetime.datetime, float]]], float, int]:
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
            percentage_trade_return = (
                (selling_shares_value - invested_amount)/invested_amount)*100

            current_balance += trade_return - 5
            commissions += COMMISSION
            number_of_trade += 1
            # Save updated balance to file
            save_balance_to_file(current_balance)

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
    ax.scatter(data.index, data['Buy_Signal'], color='green',
               marker='^', label='Buy Signal', alpha=1)
    ax.scatter(data.index, data['Sell_Signal'], color='red',
               marker='v', label='Sell Signal', alpha=1)

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
    bollinger_bands = [lines["Upper Band"],
                       lines["Middle Band"], lines["Lower Band"]]
    moving_average_lines = [lines["SMA10"], lines["SMA45"]]

    # positioning of the button for moving averages
    button_mal = fig.add_axes([0.65, 0.01, 0.1, 0.05])
    button_ma = Button(button_mal, "Toggle MAs",
                       color='lightgoldenrodyellow', hovercolor='0.975')
    button_ma.on_clicked(lambda event: toggle_visibility(
        event, moving_average_lines))

    # positioning of the button for Bollinger Bands
    button_axes = fig.add_axes([0.8, 0.01, 0.1, 0.05])
    button_bb = Button(button_axes, "Toggle Bands",
                       color='lightgoldenrodyellow', hovercolor='0.975')
    button_bb.on_clicked(
        lambda event: toggle_visibility(event, bollinger_bands))

    plt.show()


def sharpe_ratio(returns, risk_free_rate=RISKFREERATE, trading_days=252):
    excess_returns = returns - risk_free_rate / \
        trading_days  # assuming annual risk-free rate
    sharpe_ratio = excess_returns.mean() / excess_returns.std()
    return sharpe_ratio * (trading_days ** 0.5)


def treynor_ratio(returns, market_returns, beta=BETA, risk_free_rate=RISKFREERATE):
    excess_returns = returns.mean() - risk_free_rate
    market_excess_return = market_returns.mean() - risk_free_rate
    beta = excess_returns / market_excess_return
    treynor_ratio = excess_returns / beta
    return treynor_ratio


def main():
    ticker = input("Enter the stock ticker (e.g. AAPL): ")
    start_date = datetime.datetime(*date_start)
    end_date = datetime.datetime.now()
    # Calculate number of years, accounting for leap years
    years = round(((end_date - start_date).days / 365.25), 2)

    data = fetch_stock_data(ticker, start_date, end_date)
    data = preprocess_data(data)
    data = compute_signals(data)
    data = compute_daily_returns(data)
    trades, commissions, number_of_trade = compute_trade_performance(data)

    # Load end balance from file or trades
    end_balance = trades[-1]['Balance_After_Trade'] if trades else load_balance_from_file()
    display_trades(trades)

    annualized_return = calculate_annualized_return(
        CAPITAL, end_balance, years)
    market_data = fetch_market_data(start_date, end_date)
    compute_market_daily_returns(market_data)
    yoy_return = calculate_yoy_return(CAPITAL, end_balance)
    annualized_ret = market_annualized_return(market_data)
    market_annualized_return_final = round(annualized_ret * 100, 2)

    market_daily_returns = market_data['Market_Daily_Returns'].dropna()
    daily_returns = data['Daily_Returns'].dropna()
    s_ratio = sharpe_ratio(daily_returns)  # Portfolio's Sharpe Ratio
    # We now need the market returns for Treynor Ratio
    t_ratio = treynor_ratio(daily_returns, market_daily_returns)
    beta_of_the_stock = compute_beta_stock(daily_returns, market_daily_returns)
    alpha = round((((annualized_return * 100) - RISKFREERATE)) -
                  beta_of_the_stock * (market_annualized_return_final - RISKFREERATE), 2)

    print('---------------------------------------------------------------')
    print(f"TICKER: {ticker.upper()}, for the period: {start_date} - Today")
    print('---------------------------------------------------------------')
    print(f"Start Balance: ${CAPITAL:.2f}")
    print(f"End Balance: ${end_balance:.2f}")
    print('---------------------------------------------------------------')
    print(f"Total commissions payed: ${commissions:.2f}")
    print(f"Total number of trade: {number_of_trade}")
    print('---------------------------------------------------------------')
    print(f"Annualized Return: {annualized_return * 100:.2f}%")
    print(f"Total Return: {yoy_return * 100:.2f}%")
    print(f"Number of years: {years}")
    print(f"Market (SPY) Annualized Return: {market_annualized_return_final}%")
    print('---------------------------------------------------------------')
    print(f"Sharpe Ratio: {s_ratio:.4f}")
    print(f"Treynor Ratio: {t_ratio:.4f}")
    print(f"Alpha : {alpha}")
    print('---------------------------------------------------------------')

    plot_stock_data(ticker, data)


if __name__ == "__main__":
    main()
