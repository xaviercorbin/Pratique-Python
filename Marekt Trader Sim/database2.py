import yfinance as yf
import sqlite3
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data = stock_data[['High', 'Low', 'Close']].copy()
        stock_data['Day_Return'] = stock_data['Close'].pct_change()
        return stock_data.reset_index()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def store_in_database(ticker, data):
    conn = sqlite3.connect('2011_stocks_future.db')
    cursor = conn.cursor()

    sanitized_ticker = ticker.replace("^", "")

    cursor.execute(f"DROP TABLE IF EXISTS {sanitized_ticker}")

    cursor.execute(f'''
        CREATE TABLE {sanitized_ticker} (
            Date TEXT PRIMARY KEY,
            High REAL,
            Low REAL,
            Close REAL,
            Day_Return REAL
        )
    ''')

    for _, row in data.iterrows():
        cursor.execute(f'''
            INSERT INTO {sanitized_ticker} (Date, High, Low, Close, Day_Return)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['Date'].strftime('%Y-%m-%d'), row['High'], row['Low'], row['Close'], row['Day_Return']))

    conn.commit()
    conn.close()

def simulate_future_stock_prices(last_known_price, mean_return, std_return):
    total_days = (datetime(2200, 1, 1) - datetime.now()).days
    random_returns = np.random.normal(mean_return, std_return, total_days)

    future_prices = [last_known_price]
    for ret in random_returns:
        future_prices.append(future_prices[-1] * (1 + ret))
    
    return future_prices

def store_future_in_database(ticker, last_known_date, future_prices):
    conn = sqlite3.connect('2011_stocks_future.db')
    cursor = conn.cursor()

    sanitized_ticker = ticker.replace("^", "")

    current_date = last_known_date
    last_price = future_prices[0]
    
    # Initialize empty lists to hold future highs and lows
    future_highs = []
    future_lows = []
    
    for idx, price in enumerate(future_prices[1:]):
        current_date += timedelta(days=1)

        # Calculate 52-week high and low if enough days have passed
        if idx >= 52:
            high = max(future_prices[idx-52:idx+1])
            low = min(future_prices[idx-52:idx+1])
        else:
            high = max(future_prices[:idx+1])
            low = min(future_prices[:idx+1])

        # Calculate the Day_Return
        day_return = (price - last_price) / last_price

        cursor.execute(f'''
            INSERT INTO {sanitized_ticker} (Date, High, Low, Close, Day_Return)
            VALUES (?, ?, ?, ?, ?)
        ''', (current_date.strftime('%Y-%m-%d'), high, low, price, day_return))

        last_price = price

    conn.commit()
    conn.close()



stocks = ['NVDA', 'TSLA', 'AAPL', 'AMD', 'NFLX', 'GPS', 'QCOM', 'AMZN', 'TD', '^GSPC']
start_date = '2011-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

for stock in stocks:
    print(f"Fetching data for {stock}...")
    data = fetch_stock_data(stock, start_date, end_date)
    if data is not None:
        store_in_database(stock, data)

        mean_return = data['Day_Return'].mean()
        std_return = data['Day_Return'].std()
        
        future_prices = simulate_future_stock_prices(data['Close'].iloc[-1], mean_return, std_return)
        
        store_future_in_database(stock, data['Date'].iloc[-1], future_prices)


print("Data fetching, storing, and future simulation completed!")
