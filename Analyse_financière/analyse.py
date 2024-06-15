import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def prepare_data(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data

def analyze_investments(data):
    value_columns = [col for col in data.columns if 'Value' in col]
    returns = data[value_columns].pct_change().dropna()
    cumulative_returns = (1 + returns).cumprod() - 1
    return cumulative_returns

def simulate_portfolios(data, num_simulations=1000):
    value_columns = [col for col in data.columns if 'Value' in col]
    results = []
    returns = data[value_columns].pct_change().dropna()

    for _ in range(num_simulations):
        weights = np.random.random(len(value_columns))
        weights /= np.sum(weights)
        
        portfolio_return = np.sum(returns.mean() * weights) * 252
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        
        results.append([portfolio_return, portfolio_std_dev, weights.tolist()])
    
    return results

def plot_cumulative_returns(cumulative_returns):
    plt.figure(figsize=(10, 6))
    for column in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[column], label=column)
    plt.title('Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.show()

def plot_portfolio_simulation(portfolio_results):
    results = np.array([[result[0], result[1], result[0] / result[1]] for result in portfolio_results])
    plt.figure(figsize=(10, 6))
    plt.scatter(results[:, 1], results[:, 0], c=results[:, 2], marker='o')
    plt.title('Portfolio Simulation')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()

if __name__ == '__main__':
    file_path = '/mnt/data/portfolio.csv'
    
    data = load_data(file_path)
    data = prepare_data(data)
    
    cumulative_returns = analyze_investments(data)
    portfolio_results = simulate_portfolios(data)
    
    plot_cumulative_returns(cumulative_returns)
    plot_portfolio_simulation(portfolio_results)
