import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pandas as pd

def toggle_bollinger_band_visibility(event, lines):
    """Toggle the visibility of the Bollinger Bands when a button is pressed."""
    for line in lines:
        line.set_visible(not line.get_visible())
    plt.draw()

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
    bollinger_bands = [lines["Upper Band"], lines["Middle Band"], lines["Lower Band"]]
    moving_average_lines = [lines["SMA10"], lines["SMA45"]]

    button_mal = fig.add_axes([0.65, 0.01, 0.1, 0.05])  # positioning of the button for moving averages
    button_ma = Button(button_mal, "Toggle MAs", color='lightgoldenrodyellow', hovercolor='0.975')
    button_ma.on_clicked(lambda event: toggle_bollinger_band_visibility(event, moving_average_lines))  # Reusing the function, as the behavior is the same

    button_axes = fig.add_axes([0.8, 0.01, 0.1, 0.05])  # positioning of the button for Bollinger Bands
    button_bb = Button(button_axes, "Toggle Bands", color='lightgoldenrodyellow', hovercolor='0.975')
    button_bb.on_clicked(lambda event: toggle_bollinger_band_visibility(event, bollinger_bands))

    plt.show()


