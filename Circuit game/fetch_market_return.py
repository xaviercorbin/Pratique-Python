# fetch_market_return.py
import yfinance as yf
import numpy as np
import datetime

RISKFREERATE = 0.0531

def fetch_market_data(start_date, end_date, market_ticker='SPY'):
    """Fetches market data for the given ticker and dates."""
    try:
        return yf.download(market_ticker, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

def compute_daily_returns(data):
    """Computes daily returns based on close prices for market data."""
    data['Market_Daily_Returns'] = data['Close'].pct_change()
    return data

def market_annualized_return(data):
    """Calculates the market's annualized return."""
    years = (data.index[-1] - data.index[0]).days / 365.25
    if years == 0:
        return 0
    total_return = (data['Close'][-1] / data['Close'][0]) - 1
    return (1 + total_return) ** (1 / years) - 1

def fetch_stock_data(ticker, start_date, end_date):
    """Fetches stock data for the given ticker and dates."""
    try:
        return yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

if __name__ == "__main__":
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime.now()
    market_data = fetch_market_data(start_date, end_date)
    market_data = compute_daily_returns(market_data)
    #annualized_ret = market_annualized_return(market_data)
    #print(f"Market (SPY) Annualized Return: {annualized_ret * 100:.2f}%")
