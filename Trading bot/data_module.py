import yfinance as yf
import pandas as pd
import statsmodels.api as sm

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

# BETA
def calculate_beta(data, market_returns):
    # Assuming 'Returns' is a column in your 'data' dataframe
    # and you've already calculated the daily returns.
    X = market_returns
    y = data['Returns']
    X1 = sm.add_constant(X)

    model = sm.OLS(y, X1)
    results = model.fit()

    # The beta value
    beta = results.params[1]
    return beta

