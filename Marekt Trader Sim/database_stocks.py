import yfinance as yf
import sqlite3
from datetime import datetime

# Define a function to fetch the stock data
def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data = stock_data[['High', 'Low', 'Close']].copy()  # Use .copy() to prevent the SettingWithCopyWarning
        # Calculate day return
        stock_data['Day_Return'] = stock_data['Close'].pct_change()
        return stock_data.reset_index()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def store_in_database(ticker, data):
    conn = sqlite3.connect('2011_stocks.db')
    cursor = conn.cursor()

    sanitized_ticker = ticker.replace("^", "")  # Handle special character

    # Drop the table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {sanitized_ticker}")

    # (Re)Create the table
    cursor.execute(f'''
        CREATE TABLE {sanitized_ticker} (
            Date TEXT PRIMARY KEY,
            High REAL,
            Low REAL,
            Close REAL,
            Day_Return REAL
        )
    ''')

    # Insert the stock data
    for _, row in data.iterrows():
        cursor.execute(f'''
            INSERT INTO {sanitized_ticker} (Date, High, Low, Close, Day_Return)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['Date'].strftime('%Y-%m-%d'), row['High'], row['Low'], row['Close'], row['Day_Return']))

    conn.commit()
    conn.close()

# Define the stocks and the date range
stocks = ['NVDA', 'TSLA', 'AAPL', 'AMD', 'NFLX', 'GPS', 'QCOM', 'AMZN', 'TD', '^GSPC']  # Added S&P 500 index as ^GSPC
start_date = '2011-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

# Fetch and store the stock data
for stock in stocks:
    print(f"Fetching data for {stock}...")
    data = fetch_stock_data(stock, start_date, end_date)
    if data is not None:
        store_in_database(stock, data)

print("Data fetching and storing completed!")
