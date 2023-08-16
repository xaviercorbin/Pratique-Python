import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
import random
import matplotlib

class TransferMoney(tk.Toplevel):

    def __init__(self, parent, cash_available):
        super().__init__(parent)

        self.parent = parent
        self.cash_available = cash_available
        self.transfer_amount_var = tk.StringVar()

        self.lbl_cash = tk.Label(self, text=f"${self.cash_available:.2f}", font=('Arial', 16))
        self.lbl_cash.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        self.lbl_cash_title = tk.Label(self, text="Cash Available", font=('Arial', 10))
        self.lbl_cash_title.grid(row=1, column=0, sticky='w', padx=10)

        self.slider = ttk.Scale(self, from_=0, to_=1, orient="horizontal", command=self.update_slider)
        self.slider.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        self.slider.set(0)

        self.lbl_transfer_amount = tk.Label(self, text="$0.00", font=('Arial', 16, 'bold'))
        self.lbl_transfer_amount.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.entry_transfer = tk.Entry(self, textvariable=self.transfer_amount_var)
        self.entry_transfer.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.btn_transfer = tk.Button(self, text="Deposit", command=self.make_transfer)
        self.btn_transfer.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def update_slider(self, value):
        """Updates interface based on slider's position."""
        if float(value) <= 0.5:
            self.btn_transfer.config(text="Deposit", bg="green")
            self.slider.configure(style="Green.Horizontal.TScale")
        else:
            self.btn_transfer.config(text="Withdraw", bg="red")
            self.slider.configure(style="Red.Horizontal.TScale")

    def make_transfer(self):
        """Handle deposit or withdraw operation."""
        amount = float(self.transfer_amount_var.get())
        if self.btn_transfer.cget("text") == "Deposit":
            self.parent.cash += amount
        else:
            self.parent.cash -= amount
        self.parent.update_cash_display()
        self.destroy()

class TradingSimulator(tk.Tk):

    def __init__(self):
        super().__init__()

        self.cash = 10000.00  # Example cash amount
        
        self.title("Stock Market Simulator")
        
        self.current_date = date.today()
        
        # Cash amount in bank
        self.lbl_cash = tk.Label(self, text="$10,000.00", font=('Arial', 16))
        self.lbl_cash.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # Energy remaining
        self.lbl_energy = tk.Label(self, text="Energy: 100/100", font=('Arial', 10))
        self.lbl_energy.grid(row=1, column=0, sticky='w', padx=10)

        # END DAY button
        self.btn_end_day = tk.Button(self, text="END DAY", command=self.end_day)
        self.btn_end_day.grid(row=0, column=1, sticky='e', padx=10, pady=10)

        # Current day
        self.lbl_day = tk.Label(self, text="formatted_date", font=('Arial', 10))
        self.lbl_day.grid(row=1, column=1, sticky='e', padx=10)

        # Portfolio details
        self.lbl_portfolio_title = tk.Label(self, text="Portfolio", font=('Arial', 14))
        self.lbl_portfolio_title.grid(row=3, column=0, sticky='w', padx=10, pady=10)
        
        self.lbl_portfolio_value = tk.Label(self, text="$10,000.00", font=('Arial', 14))
        self.lbl_portfolio_value.grid(row=4, column=0, sticky='w', padx=10)
        
        self.lbl_portfolio_change = tk.Label(self, text="$235.34 (2.35%) Today - Market Open", font=('Arial', 10))
        self.lbl_portfolio_change.grid(row=6, column=0, sticky='w', padx=10)

        # Small buttons on the right
        self.btn_add = tk.Button(self, text="+", command=self.open_transfer_window)
        self.btn_add.grid(row=4, column=1)
        
        style = ttk.Style()
        style.configure("Green.Horizontal.TScale", background="green")
        style.configure("Red.Horizontal.TScale", background="red")

        self.btn_graph = tk.Button(self, text="📊")
        self.btn_graph.grid(row=4, column=2)

        self.btn_search = tk.Button(self, text="🔍")
        self.btn_search.grid(row=4, column=4)

        # Here you'll place the linear graph

        # Example for a security in portfolio
        self.lbl_security = tk.Label(self, text="MAST 3000 shares")
        self.lbl_security.grid(row=8, column=0, padx=10, pady=5, sticky='w')

        # Footer menu buttons (icon placeholders for now)
        self.btn_menu1 = tk.Button(self, text="")
        self.btn_menu1.grid(row=9, column=0)
        
        self.btn_menu2 = tk.Button(self, text="2")
        self.btn_menu2.grid(row=9, column=1)
        
        self.btn_menu3 = tk.Button(self, text="3")
        self.btn_menu3.grid(row=9, column=2)

        self.btn_menu4 = tk.Button(self, text="4")
        self.btn_menu4.grid(row=9, column=3)

        self.btn_menu5 = tk.Button(self, text="Cheats")
        self.btn_menu5.grid(row=9, column=4)
        
        self.update_displayed_date()
    
    def update_cash_display(self):
       self.lbl_cash.config(text=f"${self.cash:.2f}")

    def open_transfer_window(self):
        TransferMoney(self, self.cash)
    
    def update_displayed_date(self):
        formatted_date = self.current_date.strftime("%A, %b %d, %Y")
        self.lbl_day.config(text=formatted_date)
    
    def update_displayed_prices(self):
        pass    

    def end_day(self):
        self.current_date += timedelta(days=1)
        self.update_displayed_date()
        
        
        pass

if __name__ == "__main__":
    app = TradingSimulator()
    app.mainloop()
