import numpy as np
import pandas as pd
from data_module import calculate_beta
from utils import save_balance_to_file, load_balance_from_file, CAPITAL, COMMISSION
import data_module

# SIGNALS
def compute_signals(data):
    """Computes buy and sell signals based on moving average crossover."""
    data['Buy_Signal'] = np.where(
        (data['SMA10'] > data['SMA45']) & (data['SMA10'].shift(1) <= data['SMA45'].shift(1)), 
        data['Close'], np.nan)

    data['Sell_Signal'] = np.where(
        (data['SMA10'] < data['SMA45']) & (data['SMA10'].shift(1) >= data['SMA45'].shift(1)), 
        data['Close'], np.nan)

    return data

# COMPUTING TRADES
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

# RETURN
def calculate_annualized_return(start_balance, end_balance, years):
    if years == 0:  # Prevent division by zero
        return 0
    return (end_balance / start_balance) ** (1 / years) - 1

def calculate_yoy_return(start_balance, end_balance):
    return (end_balance - start_balance) / start_balance


# RATIOS
def maximum_drawdown(timeseries):
    cumulative_returns = (1 + timeseries).cumprod()
    running_max = cumulative_returns.cummax()
    drawdowns = (cumulative_returns - running_max) / running_max
    return drawdowns.min()

def sharpe_ratio(returns, risk_free_rate=0.03, trading_days=252):
    excess_returns = returns - risk_free_rate / trading_days  # assuming annual risk-free rate
    sharpe_ratio = excess_returns.mean() / excess_returns.std()
    return sharpe_ratio * (trading_days ** 0.5)

def treynor_ratio(returns, beta, risk_free_rate=0.03):
    excess_returns = returns.mean() - risk_free_rate
    treynor_ratio = excess_returns / beta
    return treynor_ratio

market_data = fetch_stock_data('SPY', start_date, end_date)  # Assuming 'SPY' as a proxy for S&P 500
market_returns = market_data['Close'].pct_change().dropna()
data['Returns'] = data['Close'].pct_change()

beta = calculate_beta(data, market_returns)
