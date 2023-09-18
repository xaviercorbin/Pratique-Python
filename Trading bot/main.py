import datetime
import pandas as pd
from data_module import fetch_stock_data, preprocess_data
from trading_module import compute_signals, compute_trade_performance, calculate_annualized_return, calculate_yoy_return
from trading_module import macimum_drawdown, sharpe_ratio, treynor_ratio
from visualization_module import plot_stock_data, display_trades, toggle_bollinger_band_visibility
from utils import save_balance_to_file, load_balance_from_file, CAPITAL, COMMISSION

date_start = (2010, 1, 1)

def main():
    ticker = input("Enter the stock ticker (e.g. AAPL): ")
    start_date = datetime.datetime(*date_start)
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
    
    daily_returns = data['Close'].pct_change().dropna()
    md = maximum_drawdown(daily_returns)
    sr = sharpe_ratio(daily_returns)
    tr = treynor_ratio(daily_returns, beta)

    print(f"Maximum Drawdown: {md:.2f}")
    print(f"Sharpe Ratio: {sr:.2f}")
    print(f"Treynor Ratio: {tr:.2f}")


    plot_stock_data(ticker, data)

if __name__ == "__main__":
    main()
