import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def best_period_for_stock(stock):
    conn = sqlite3.connect('stocks.db')
    df = pd.read_sql(f'SELECT * FROM {stock}', conn)
    conn.close()

    df['Log_Return'] = (1 + df['Day_Return']).apply(lambda x: 0 if x == 0 else np.log(x))
    df['Cum_Log_Return'] = df['Log_Return'].cumsum()
    
    max_end = df['Cum_Log_Return'].idxmax()
    if df['Day_Return'].iloc[0] == df['Cum_Log_Return'].iloc[max_end]:
        max_start = 0
    else:
        max_start = df['Cum_Log_Return'].iloc[:max_end].idxmin() + 1
    
    return df['Date'].iloc[max_start], df['Date'].iloc[max_end], df['Cum_Log_Return'].iloc[max_end] - df['Cum_Log_Return'].iloc[max_start]

stocks_without_market = ['NVDA', 'TSLA', 'AAPL', 'AMD', 'TNET', 'NFLX', 'GPS', 'DELL', 'QCOM']

best_periods = {}
for stock in stocks_without_market:
    start, end, return_ = best_period_for_stock(stock)
    best_periods[stock] = (start, end, return_)

sorted_stocks = sorted(best_periods.items(), key=lambda x: x[1][2], reverse=True)

# Plotting
fig, ax = plt.subplots(figsize=(15, 10))

# Setting a color palette
colors = plt.cm.viridis(np.linspace(0, 1, len(sorted_stocks)))

for index, (stock, (start, end, return_)) in enumerate(sorted_stocks):
    ax.plot([start, end], [index, index], color=colors[index], linewidth=6, label=f'{stock} ({return_*100:.2f}%)')

ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.set_yticks(range(len(sorted_stocks)))
ax.set_yticklabels([item[0] for item in sorted_stocks])

ax.set_xlabel('Date')
ax.set_title('Best Period for Stocks')
ax.legend()

plt.tight_layout()
plt.gca().invert_yaxis()  # To have the highest returns at the top
plt.grid(True, axis='x', linestyle='--', linewidth=0.7, alpha=0.6)
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.show()
