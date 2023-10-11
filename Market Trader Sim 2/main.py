# main.py

from imports import *
from globals import *
from functions import *

# ... (Main game logic, layout, and loop goes here)




# Upper header
money_label = customtkinter.CTkLabel(
    master=homepage, text="$" + "{:,}".format(money), font=("Arial", 55), anchor='w', width=15)
money_label.grid(row=0, column=0, columnspan=3,
                 sticky='w', padx=(100, 0), pady=(40, 20))

energy_label = customtkinter.CTkLabel(
    master=homepage, text="⚡" + str(energy) + "/2355", font=("Arial", 20), anchor='w')
energy_label.grid(row=1, column=0, sticky='w', padx=(100, 0), pady=(0, 40))

day_label = customtkinter.CTkLabel(
    master=homepage, text=formatted_date, font=("Arial", 20), anchor='w')
day_label.grid(row=1, columnspan=2, column=3,
               sticky='w', padx=(100, 0), pady=(0, 40))

end_day_button = customtkinter.CTkButton(master=homepage, text='END DAY', font=(
    "Arial", 25), width=12, command=advance_day)
end_day_button.grid(row=0, rowspan=2, column=4,  columnspan=1,
                    sticky='E', padx=(0, 100), pady=(40, 40))

# Portfolio section
portfolio_label = customtkinter.CTkLabel(
    master=homepage, text="Portfolio", font=('Arial', 40), anchor='w')
portfolio_label.grid(row=2, column=0, sticky='w', padx=(100, 0), pady=(40, 20))

portfolio_value_label = customtkinter.CTkLabel(
    master=homepage, text="$" + "{:,}".format(portfolio_value), font=('Arial', 35), anchor='w', width=25)
portfolio_value_label.grid(row=3, column=0, sticky='w', padx=(100, 0))

today_change_label = customtkinter.CTkLabel(
    master=homepage, text=f"{dollar_change} | {percentage_change} Today", font=("Arial", 20), anchor='w')
today_change_label.grid(row=4, column=0, sticky='w',
                        padx=(100, 0), pady=(40, 40))

transfer_money_button = customtkinter.CTkButton(
    master=homepage, text='➕', font=("Arial", 24), width=12, command=transfer_money)
transfer_money_button.grid(row=3, column=2, sticky='E',
                           padx=(0, 100), pady=(40, 40))

performance_button = customtkinter.CTkButton(
    master=homepage, text='📈', font=("Arial", 24), width=12, command=performance)
performance_button.grid(row=3, column=3, sticky='E',
                        padx=(0, 100), pady=(40, 40))

markets_button = customtkinter.CTkButton(
    master=homepage, text='🔍', font=("Arial", 24), width=12, command=markets)
markets_button.grid(row=3, column=4, sticky='E', padx=(0, 100), pady=(40, 40))

# Bottom buttons
icons = [('💲', home_page), ('👤', bonus), ('📊', finances),
         ('🏠', lifestyle), ('🎛️', cheats)]
for idx, (icon, cmd) in enumerate(icons):
    btn = customtkinter.CTkButton(
        master=homepage, text=icon, command=cmd, font=("Arial", 28), width=6)
    btn.grid(row=5, column=idx, padx=(100, 100), pady=(40, 20))

homepage.mainloop()