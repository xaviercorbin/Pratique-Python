import random
from datetime import date, timedelta

# Third-party imports (make sure they are installed)
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tkinter related imports
import tkinter as tk

class TraderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TRADER")
        self.attributes('-fullscreen', True)
        
        # Constants for initial values
        self.START_DATE = date(2011, 1, 3)
        self.START_MONEY = 93528973
        self.START_PORTFOLIO_VALUE = 3736405124
        self.START_ENERGY = 2355
        
        self.current_date = self.START_DATE
        self.money = self.START_MONEY
        self.portfolio_value = self.START_PORTFOLIO_VALUE
        self.energy = self.START_ENERGY
        
        self.create_ui()
    
    def create_ui(self):
        self.create_header()
        self.create_portfolio_section()
        self.create_bottom_buttons()
    
    def create_header(self):
        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X, padx=100, pady=(40, 20))
        
        money_label = self.create_label(header_frame, f"${self.money:,}", ("Arial", 55), 'w', 15)
        money_label.grid(row=0, column=0, columnspan=3, sticky='w')
        
        energy_label = self.create_label(header_frame, f"⚡{self.energy}/2355", ("Arial", 20), 'w')
        energy_label.grid(row=1, column=0, sticky='w')
        
        self.day_label = self.create_label(header_frame, self.get_formatted_date(), ("Arial", 20), 'w')
        self.day_label.grid(row=1, columnspan=2, column=3, sticky='w')
        
        self.create_button(header_frame, 'END DAY', ("Arial", 25), 12, self.advance_day, 'E', rowspan=2, column=4)
    
    def create_portfolio_section(self):
        portfolio_frame = tk.Frame(self)
        portfolio_frame.pack(padx=100)
        
        self.create_label(portfolio_frame, "Portfolio", ('Arial', 40), 'w')
        self.portfolio_value_label = self.create_label(portfolio_frame, f"${self.portfolio_value:,}", ('Arial', 35), 'w', 25)
        self.create_label(portfolio_frame, "0 | 0% Today", ("Arial", 20), 'w')
        
        self.create_button(portfolio_frame, '➕', ("Arial", 24), 12, self.transfer_money, 'E', column=1)
        self.create_button(portfolio_frame, '📈', ("Arial", 24), 12, self.performance, 'E', column=2)
        self.create_button(portfolio_frame, '🔍', ("Arial", 24), 12, self.markets, 'E', column=3)
    
    def create_bottom_buttons(self):
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=(40, 20))
        
        button_icons = {'💲': self.home_page, '👤': self.bonus, '📊': self.finances, '🏠': self.lifestyle, '🎛️': self.cheats}
        
        for idx, (icon, cmd) in enumerate(button_icons.items()):
            self.create_button(bottom_frame, icon, ("Arial", 28), 6, cmd, column=idx, padx=20)
    
    def create_label(self, parent, text, font, anchor, width=None):
        label = tk.Label(parent, text=text, font=font, anchor=anchor, width=width)
        return label
    
    def create_button(self, parent, text, font, width, command, sticky, rowspan=None, column=None):
        button = tk.Button(parent, text=text, font=font, width=width, command=command)
        if rowspan:
            button.grid(rowspan=rowspan, column=column, sticky=sticky)
        else:
            button.grid(column=column, sticky=sticky)
    
    def get_formatted_date(self):
        return self.current_date.strftime("%A, %b %d, %Y")
    
    def advance_day(self):
        self.current_date += timedelta(days=1)
        self.day_label.config(text=self.get_formatted_date())
    
    def transfer_money(self):
        # Implement the transfer money logic here
        print('Transfering money window')
        transfer_money_frame = customtkinter.CTk()
        transfer_money_frame.title("Transfer Money")
        
        deposit_button = self.create_button(transfer_money_frame, 'Deposit', ("Arial", 24), None, self.deposit, None)
        deposit_button.pack(pady=20)
        
        withdraw_button = self.create_button(transfer_money_frame, 'Withdraw', ("Arial", 24), None, self.withdraw, None)
        withdraw_button.pack(pady=20)
        
        transfer_money_frame.mainloop()
    
    def deposit(self):
        # Implement deposit logic here
        pass
    
    def withdraw(self):
        # Implement withdraw logic here
        pass
    
    def performance(self):
        # Implement the performance logic here
        print('Performances window open')
        
    def markets(self):
        # Implement the markets logic here
        print('Markets Window Open')
        markets_frame = customtkinter.CTk()
        markets_frame.title('Market View')
        markets_frame.mainloop()
    
    def home_page(self):
        # Implement the home page logic here
        print('Returning to HomePage')
        pass
    
    def bonus(self):
        # Implement the bonus logic here
        print('Bonus window')
        pass
    
    def finances(self):
        # Implement the finances logic here
        print('Finances window')
        pass
    
    def lifestyle(self):
        # Implement the lifestyle logic here
        print('Lifestyle window')
        pass
    
    def close_game(self):
        print('Game closed')
        # Make a saving method here if needed
        self.quit()
    
    def cheats(self):
        # Implement the cheats logic here
        cheats_frame = customtkinter.CTk()
        cheats_frame.title("Cheats Window")
        
        close_button = self.create_button(cheats_frame, 'Close the Game', ("Arial", 20), 10, self.close_game, None)
        close_button.grid(row=0, column=0)
        
        cheats_frame.mainloop()

if __name__ == "__main__":
    app = TraderApp()
    app.mainloop()
