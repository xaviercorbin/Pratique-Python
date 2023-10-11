import tkinter as tk
from tkinter import ttk, Canvas
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

def fetch_data_for_graph(ticker, start_date, end_date):
    conn = sqlite3.connect('2011_stocks_future.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT Date, Close FROM {ticker} WHERE Date BETWEEN ? AND ?", (start_date, end_date))
    data = cursor.fetchall()
    conn.close()
    return data

def plot_graph(data, ticker):
    dates, prices = zip(*data)
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(dates, prices, color="orange", linewidth=2)
    ax.set_title(ticker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    return fig

class MarketWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Title and basic layout
        self.title("Markets")
        
        # Go back button
        back_button = ttk.Button(self, text="<", command=self.destroy)  # Go back to the homepage
        back_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Market Label
        market_label = ttk.Label(self, text="Markets")
        market_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Fetch data for GSPC from the database
        today = datetime.strptime('2011-01-03', '%Y-%m-%d')
        three_months_ago = today - timedelta(days=90)
        data = fetch_data_for_graph('^GSPC', three_months_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

        if data:
            today_price = data[-1][1]
            prev_day_price = data[-2][1] if len(data) > 1 else today_price
            percent_change = ((today_price - prev_day_price) / prev_day_price) * 100

            # Market Value Label
            market_value = ttk.Label(self, text=f"${today_price:,.2f}")
            market_value.grid(row=1, column=1, padx=10, pady=10)
            
            # Percentage Change Label
            color = "green" if percent_change >= 0 else "red"
            percent_change_label = ttk.Label(self, text=f"{percent_change:.2f}%", foreground=color)
            percent_change_label.grid(row=2, column=1, padx=10, pady=10)

            # Plot the graph for GSPC
            fig = plot_graph(data, '^GSPC')
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=3, column=1, padx=10, pady=10)
        
        # Fetch all stock tickers from the database
        conn = sqlite3.connect('2011_stocks_future.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tickers = [ticker[0] for ticker in cursor.fetchall() if ticker[0] != '^GSPC']
        conn.close()

        # Display each stock ticker as a button
        for idx, ticker in enumerate(all_tickers):
            stock_button = ttk.Button(self, text=ticker, command=lambda t=ticker: self.open_stock_page(t))
            stock_button.grid(row=4+idx, column=0, padx=10, pady=10)

            cursor.execute(f"SELECT Close FROM {ticker} WHERE Date = ?", (today.strftime('%Y-%m-%d'),))
            today_price = cursor.fetchone()[0]
            cursor.execute(f"SELECT Close FROM {ticker} WHERE Date < ?", (today.strftime('%Y-%m-%d'),))
            prev_day_price = cursor.fetchone()[0] if cursor.fetchone() else today_price
            percent_change = ((today_price - prev_day_price) / prev_day_price) * 100
            color = "green" if percent_change >= 0 else "red"
            percent_change_label = ttk.Label(self, text=f"{percent_change:.2f}%", background=color)
            percent_change_label.grid(row=4+idx, column=1, padx=10, pady=10)

    def open_stock_page(self, ticker):
        # Logic to open stock detail page
        pass

app = MarketWindow()
app.mainloop()