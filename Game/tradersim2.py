import random
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk

import customtkinter
import matplotlib

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

homepage = customtkinter.CTk()
homepage.title("TRADER")
screen_width = homepage.winfo_screenwidth()
screen_height = homepage.winfo_screenheight()

# Pour essayer de centrer la fenêtre au centre
x = int(screen_width/2 - 500/2)
y = int(screen_height/2 - 350/2)
homepage.geometry(f"725x600+{x}+{y}")

#Fonction to go to the next day
def advance_day():
    print('Advanced to the next day')
    pass

#Fonction transfer money
def transfer_money():
    print('Transfering money window')
    
    transfer_money_frame = customtkinter.CTk()
    transfer_money_frame.title("Transfer Money")
    transfer_money_frame.geometry(f"725x600+{x}+{y}")
    
    def deposit():
        customtkinter.set_default_color_theme('green')
        pass
    
    def withdraw():
        customtkinter.set_default_color_theme('dark-blue')
        pass
    
    
    #Page title
    title_transfert_money = customtkinter.CTkLabel(master=transfer_money_frame, text='Transfert Money', font=("Arial", 30))
    title_transfert_money.grid(row=0, column=1)
    
    #Money available
    money_label_transfer = customtkinter.CTkLabel(master=transfer_money_frame, text="$" + str(money), font=("Arial", 26))
    money_label_transfer.grid(row=2, column=0)
    
    #Deposit button
    deposit_button = customtkinter.CTkButton(master=transfer_money_frame, text='Deposit', command=deposit)
    deposit_button.grid(row=2, column=3)
    
    #Withdraw button
    withdraw_button = customtkinter.CTkButton(master=transfer_money_frame, text='Withdraw', command=withdraw)
    withdraw_button.grid(row=2, column=4)
    
    
    
    
 
    transfer_money_frame.mainloop()
    pass

#fonction performance
def performance():
    print('Performances window open')
    pass

#Fonction markets
def markets():
    print('Markets window open')
    pass

#Fonction boutton pour aller homepage
def home_page():
    print('Returnning to HomePage')
    pass

#Fonction aller aux bonus
def bonus():
    print('Bonus window')
    pass

#fonction aller aux finances
def finances():
    print('Finances window')
    pass

#Fonction aller aux lifestyle
def lifestyle():
    print('Lifestyle window')
    pass

#Fonction aller au cheats
def cheats():
    print('Cheats window')
    pass



# Variables
money = 10000
portfolio_value = 0
energy = 100
dollar_change = 0
percentage_change = 0


#Money available
money_label = customtkinter.CTkLabel(master=homepage, text="$" + str(money), font=("Arial", 20))
money_label.grid(row=0, column=0, columnspan=2)

#Energy Available
energy_label = customtkinter.CTkLabel(master=homepage, text="⚡" +str(energy) + "/100", font=("Arial",12))
energy_label.grid(row=1, column=0, columnspan=2)

#END DAY BUTTON
end_day_button = customtkinter.CTkButton(master=homepage, text='END DAY', command=advance_day)
end_day_button.grid(row=0,column=4, sticky='W', padx=2)

#Transfer Money Button
transfer_money_button = customtkinter.CTkButton(master=homepage, text='➕', command=transfer_money)
transfer_money_button.grid(row=5, column=2, sticky='W', padx=2)

#Performance Button
performance_button = customtkinter.CTkButton(master=homepage, text='📈', command=performance)
performance_button.grid(row=5, column=3, sticky='W', padx=2)

#Market Button
markets_button = customtkinter.CTkButton(master=homepage, text='🔍', command=markets)
markets_button.grid(row=5, column=4, sticky='W', padx=2)

#Portfolio Value
portfolio_label = customtkinter.CTkLabel(master=homepage, text='Portfolio', font=('Arial', 30))
portfolio_label.grid(row=4, column=0, columnspan=2)
portfolio_value_label=customtkinter.CTkLabel(master=homepage, text="$" + str(portfolio_value), font=('Arial', 30))
portfolio_value_label.grid(row=5, column=0, columnspan=2)

#Today's Change
today_change_label = customtkinter.CTkLabel(master=homepage, text= str(dollar_change)+" "+str(percentage_change)+" Today", font=("Arial", 12))
today_change_label.grid(row=6, column=0, sticky='W')

#Graph of the last 30 days


#List of positions


#Homepage Button
home_page_button = customtkinter.CTkButton(master=homepage, text='💲', command=home_page)
home_page_button.grid(row=9, column=0, sticky='W', padx=2)

#Bonuses Button
bonus_page_button = customtkinter.CTkButton(master=homepage, text='👤', command=bonus)
bonus_page_button.grid(row=9, column=1, sticky='W', padx=2)

#Finances button
finance_page_button = customtkinter.CTkButton(master=homepage, text='📊', command=finances)
finance_page_button.grid(row=9, column=2, sticky='W', padx=2)

#Lifestyle Button
lifestyle_page_button = customtkinter.CTkButton(master=homepage, text='🏠', command=lifestyle)
lifestyle_page_button.grid(row=9, column=3, sticky='W', padx=2)

#Cheats Button
cheats_page_button = customtkinter.CTkButton(master=homepage, text='🎛️', command=cheats)
cheats_page_button.grid(row=9, column=4, sticky='W', padx=2)






homepage.mainloop()