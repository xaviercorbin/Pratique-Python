import random
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk, IntVar

import customtkinter
import matplotlib

print('Game started')

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

homepage = customtkinter.CTk()
homepage.title("TRADER")
homepage.attributes('-fullscreen', True) 

current_date = date(2011, 1, 3)

# Update money value
def update_money_label():
    money_label['text'] = "$" + "{:,}".format(money)

def update_portfolio_value_label():
    portfolio_value_label['text'] = "$" + "{:,}".format(portfolio_value)




# Fonction to go to the next day

def advance_day():
    global current_date
    print('Advanced to the next day')
    current_date = current_date + timedelta(days=1)
    formatted_date = current_date.strftime("%A, %b %d, %Y")
    day_label.configure(text=formatted_date)

# Fonction transfer money



def deposit():
    global money, portfolio_value
    # Logic for depositing money
    print("Depositing money")
    deposit_frame = customtkinter.CTk()
    deposit_frame.title("Deposit Money")
    
    def finalize_deposit():
        global portfolio_value, money
        print('Finalized deposit')
        amount = float(amount_entry.get())
        portfolio_value += amount
        money -= amount
        print(f"Deposited ${amount}. New portfolio value: ${portfolio_value}. Remaining money: ${money}")
        update_money_label()
        update_portfolio_value_label()
        deposit_frame.destroy()

    
    # Close Button
    close_button = customtkinter.CTkButton(master=deposit_frame, text='X', command=deposit_frame.destroy)
    close_button.grid(row=0, column=0, sticky='E', padx=(0, 20), pady=(10, 10))

    # Title
    title_transfert_money = customtkinter.CTkLabel(
        master=deposit_frame, text='Deposit Money', font=("Arial", 30))
    title_transfert_money.grid(row=1, column=0, columnspan=5, pady=20)

    # Money available
    money_label_transfer = customtkinter.CTkLabel(
        master=deposit_frame, text="$" + "{:,}".format(money), font=("Arial", 40))
    money_label_transfer.grid(row=2, column=0, columnspan=5)

    # Entry to input deposit amount
    amount_label = customtkinter.CTkLabel(master=deposit_frame, text='Enter an amount:', font=("Arial", 16))
    amount_label.grid(row=4, column=0, columnspan=5, pady=(20, 0))
    amount_entry = customtkinter.CTkEntry(master=deposit_frame, font=("Arial", 20))
    amount_entry.grid(row=5, column=0, columnspan=5, padx=20, pady=10)

    # Button to finalize the deposit
    finalize_button = customtkinter.CTkButton(master=deposit_frame, text='Finalize Deposit', font=("Arial", 20), command=finalize_deposit)
    finalize_button.grid(row=6, column=0, columnspan=5, padx=20, pady=20)

    deposit_frame.mainloop()

def withdraw():
    # Logic for withdrawing money
    print("Withdrawing money")
    global money, portfolio_value
    # Logic for withdrawing money
    print("Withdrawing money")
    withdraw_frame = customtkinter.CTk()
    withdraw_frame.title("Withdraw Money")
    
    def finalize_withdraw():
        print('Finalized withdraw')
        global money, portfolio_value
        amount = float(amount_entry.get())
        if amount > portfolio_value:
            print(f"Cannot withdraw ${amount}. Exceeds portfolio value.")
            return
        portfolio_value -= amount
        money += amount
        print(f"Withdrew ${amount}. New portfolio value: ${portfolio_value}. Remaining money: ${money}")
        update_money_label()
        update_portfolio_value_label()
        withdraw_frame.destroy()

    # Close Button
    close_button = customtkinter.CTkButton(master=withdraw_frame, text='X', command=withdraw_frame.destroy)
    close_button.grid(row=0, column=0, sticky='E', padx=(0, 20), pady=(10, 10))

    # Title
    title_transfert_money = customtkinter.CTkLabel(
        master=withdraw_frame, text='Deposit Money', font=("Arial", 30))
    title_transfert_money.grid(row=1, column=0, columnspan=5, pady=20)

    # Money available
    money_label_transfer = customtkinter.CTkLabel(
        master=withdraw_frame, text="$" + "{:,}".format(money), font=("Arial", 40))
    money_label_transfer.grid(row=2, column=0, columnspan=5)

    # Entry to input deposit amount
    amount_label = customtkinter.CTkLabel(master=withdraw_frame, text='Enter an amount:', font=("Arial", 16))
    amount_label.grid(row=4, column=0, columnspan=5, pady=(20, 0))
    amount_entry = customtkinter.CTkEntry(master=withdraw_frame, font=("Arial", 20))
    amount_entry.grid(row=5, column=0, columnspan=5, padx=20, pady=10)
    
    # Button to finalize the withdrawal
    finalize_button = customtkinter.CTkButton(master=withdraw_frame, text='Finalize Withdraw', font=("Arial", 20), command=finalize_withdraw)
    finalize_button.grid(row=6, column=0, columnspan=5, padx=20, pady=20)

    withdraw_frame.mainloop()
    
    
def transfer_money():
    print('Transfering money window')
    
    transfer_money_frame = customtkinter.CTk()
    transfer_money_frame.title("Transfer Money")
    
    # Creating Deposit button
    deposit_button = customtkinter.CTkButton(transfer_money_frame, text="Deposit", command=deposit)
    deposit_button.pack(pady=20)  # Add some padding to position the buttons nicely
    
    # Creating Withdraw button
    withdraw_button = customtkinter.CTkButton(transfer_money_frame, text="Withdraw", command=withdraw)
    withdraw_button.pack(pady=20)
    
    transfer_money_frame.mainloop()



# fonction performance


def performance():
    print('Performances window open')
    pass

# Fonction markets


def markets():
    print('Markets Window Open')
    markets_frame = customtkinter.ctk()
    markets_frame.title('Market View')
    
    
    

# Fonction boutton pour aller homepage


def home_page():
    print('Returnning to HomePage')
    pass

# Fonction aller aux bonus


def bonus():
    print('Bonus window')
    pass

# fonction aller aux finances


def finances():
    print('Finances window')
    pass

# Fonction aller aux lifestyle


def lifestyle():
    print('Lifestyle window')
    pass


# Fonction pour fermer le jeux
# Function to close the game
def close_game():
    print('Game closed')
    # Make a saving method here if needed
    quit()

# Function for cheats
def cheats():
    print('Cheats window')
    
    cheats_frame = customtkinter.CTk()
    cheats_frame.title("Cheats Window")
    
    close_button = customtkinter.CTkButton(master=cheats_frame, text='Close the Game', font=("Arial", 20), width=10, command=close_game)
    close_button.grid(row=0, column=0, padx=10, pady=10)  # You can adjust the padding as needed
    
    cheats_frame.mainloop()  # This keeps the window open and responsive


# Variables
money = 93528973
portfolio_value = 3736405124
energy = 2355
dollar_change = 0
percentage_change = 0

# Variable qui change avec le temps
nom = 'Connor Corbin'
age = 43
source_of_wealth = 'Self Made, Investments, Hedge Funds, Venture'
self_made_score = 8
philanthropy = '$25.3M'
residence = 'Canada'
ex_lovers = 1
martial_status = 'Married'
assets_under_management = portfolio_value
market_beat = 'You beat the market by 196.6%'
months_beat_the_market = 166
months_market_beat_you = 134
best_monthly_return = '114.9% (Jul,2036)'
worst_monthly_return = '-100.0% (Apr,2036)'
clients_signed = 33
clients_withdrawn = 18
largest_client_signed = '$3.3M'
longuest_client_signed = '2 year(s)'

formatted_date = current_date.strftime("%A, %b %d, %Y")

# Set weights for rows and columns to expand them as necessary
for i in range(6):
    homepage.rowconfigure(i, weight=1)

for i in range(5):
    homepage.columnconfigure(i, weight=1)

# Upper header
money_label = customtkinter.CTkLabel(master=homepage, text="$" + "{:,}".format(money), font=("Arial", 55), anchor='w', width=15)
money_label.grid(row=0, column=0, columnspan=3, sticky='w', padx=(100, 0), pady=(40, 20))

energy_label = customtkinter.CTkLabel(master=homepage, text="⚡" + str(energy) + "/2355", font=("Arial", 20), anchor='w')
energy_label.grid(row=1, column=0, sticky='w', padx=(100, 0), pady=(0, 40))

day_label = customtkinter.CTkLabel(master=homepage, text=formatted_date, font=("Arial", 20), anchor='w')
day_label.grid(row=1, columnspan=2, column=3, sticky='w', padx=(100, 0), pady=(0, 40))

end_day_button = customtkinter.CTkButton(master=homepage, text='END DAY', font=("Arial", 25), width=12, command=advance_day)
end_day_button.grid(row=0, rowspan=2, column=4,  columnspan=1, sticky='E', padx=(0, 100), pady=(40, 40))

# Portfolio section
portfolio_label = customtkinter.CTkLabel(master=homepage, text="Portfolio", font=('Arial', 40), anchor='w')
portfolio_label.grid(row=2, column=0, sticky='w', padx=(100, 0), pady=(40, 20))

portfolio_value_label = customtkinter.CTkLabel(master=homepage, text="$" + "{:,}".format(portfolio_value), font=('Arial', 35), anchor='w', width=25)
portfolio_value_label.grid(row=3, column=0, sticky='w', padx=(100, 0))

today_change_label = customtkinter.CTkLabel(master=homepage, text=f"{dollar_change} | {percentage_change} Today", font=("Arial", 20), anchor='w')
today_change_label.grid(row=4, column=0, sticky='w', padx=(100, 0), pady=(40, 40))

transfer_money_button = customtkinter.CTkButton(master=homepage, text='➕', font=("Arial", 24), width=12, command=transfer_money)
transfer_money_button.grid(row=3, column=2, sticky='E', padx=(0, 100), pady=(40, 40))

performance_button = customtkinter.CTkButton(master=homepage, text='📈', font=("Arial", 24), width=12, command=performance)
performance_button.grid(row=3, column=3, sticky='E', padx=(0, 100), pady=(40, 40))

markets_button = customtkinter.CTkButton(master=homepage, text='🔍', font=("Arial", 24), width=12, command=markets)
markets_button.grid(row=3, column=4, sticky='E', padx=(0, 100), pady=(40, 40))

# Bottom buttons
icons = [('💲', home_page), ('👤', bonus), ('📊', finances), ('🏠', lifestyle), ('🎛️', cheats)]
for idx, (icon, cmd) in enumerate(icons):
    btn = customtkinter.CTkButton(master=homepage, text=icon, command=cmd, font=("Arial", 28), width=6)
    btn.grid(row=5, column=idx, padx=(100, 100), pady=(40, 20))

homepage.mainloop()
