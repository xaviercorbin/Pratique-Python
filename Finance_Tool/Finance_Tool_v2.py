import os
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import customtkinter
import openpyxl
import pandas as pd
import yfinance as yf

# Beaucoup de import, mais je compte les utiliser pour des futurs trucs. Par contre, je pense qu'ils en a des inutiles qui se répètent

customtkinter.set_appearance_mode('system')
customtkinter.set_default_color_theme('dark-blue')
mainroot = customtkinter.CTk()
screen_width = mainroot.winfo_screenwidth()
screen_height = mainroot.winfo_screenheight()

# Pour essayer de centrer la fenêtre au centre
x = int(screen_width/2 - 500/2)
y = int(screen_height/2 - 350/2)
mainroot.geometry(f"500x400+{x}+{y}")
mainroot.title("Selection of Tools")


def historic_prices():
    print("User have selected : Historic Price")
    frame_historic_prices = customtkinter.CTk()
    frame_historic_prices.title('Historic Price')
    frame_historic_prices.geometry("600x200")
    option_var = customtkinter.StringVar(value='1mo')

    def period_option_menu(choice):
        period_textbox.delete(1.0, END)
        if choice == '1mo':
            period_textbox.insert(END, '1mo')
        if choice == '3mo':
            period_textbox.insert(END, '3mo')
        if choice == '6mo':
            period_textbox.insert(END, '6mo')
        if choice == 'ytd':
            period_textbox.insert(END, 'ytd')
        if choice == '1y':
            period_textbox.insert(END, '1y')
        if choice == '2y':
            period_textbox.insert(END, '2y')
        if choice == '5y':
            period_textbox.insert(END, '5y')
        if choice == '10y':
            period_textbox.insert(END, '10y')
        elif choice == 'max':
            period_textbox.insert(END, 'max')

    menu_period = customtkinter.CTkOptionMenu(master=frame_historic_prices, values=[
                                              '1mo', '3mo', '6mo', 'ytd', '1y', '2y', '5y', '10y', 'max'], command=period_option_menu, variable=option_var)
    menu_period.grid(row=4, column=3, sticky='W')

    def results_of_historic_prices():
        print('Research of historic prices for the ticker : ' +
              entry_ticker_entry.get())
        frame_results_of_historic_prices = tk.Toplevel()
        frame_results_of_historic_prices.title(
            'Results of the historic price of : ' + entry_ticker_entry.get())

        # Creation of the treeview
        historic_prices_tree = ttk.Treeview(frame_results_of_historic_prices, columns=(
            'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'))
        style = ttk.Style()
        style.theme_use("clam")

        # Set Column Headings
        historic_prices_tree.heading(
            '#0', text='Ticker', anchor='center')
        historic_prices_tree.heading(
            '#1', text='Date', anchor='center')
        historic_prices_tree.heading(
            '#2', text='Open', anchor='center')
        historic_prices_tree.heading(
            '#3', text='High', anchor='center')
        historic_prices_tree.heading('#4', text='Low', anchor='center')
        historic_prices_tree.heading(
            '#5', text='Close', anchor='center')
        historic_prices_tree.heading(
            '#6', text='Volume', anchor='center')
        historic_prices_tree.heading(
            '#7', text='Dividends', anchor='center')
        historic_prices_tree.heading(
            '#8', text='Stock Splits', anchor='center')

        # Set Column Widths
        historic_prices_tree.column('#1', width=100)
        historic_prices_tree.column('#2', width=100)
        historic_prices_tree.column('#3', width=100)
        historic_prices_tree.column('#4', width=100)
        historic_prices_tree.column('#5', width=100)
        historic_prices_tree.column('#6', width=100)
        historic_prices_tree.column('#7', width=100)
        historic_prices_tree.column('#8', width=100)

        # Insert the Data in the Treeview
        ticker_symbol = entry_ticker_entry.get()
        ticker = yf.Ticker(ticker_symbol)
        # select the period
        history = ticker.history(period=period_textbox.get('1.0', 'end-1c'))
        for i, row in history.iterrows():
            open_price = round(row['Open'], 2)
            high_price = round(row['High'], 2)
            low_price = round(row['Low'], 2)
            close_price = round(row['Close'], 2)
            volume = round(row['Volume'], 2)
            dividends = round(row['Dividends'], 2)
            stock_splits = round(row['Stock Splits'], 2)

            # insert the data into the treeview
            historic_prices_tree.insert('', 'end', text=ticker.ticker, values=(i.date(
            ), f"{open_price:^10}", f"{high_price:^10}", f"{low_price:^10}", f"{close_price:^10}", f"{volume:^10}", f"{dividends:^10}", f"{stock_splits:^10}"))

        # pack the treeview into the root window
        historic_prices_tree.pack(
            fill='both', expand=True, padx=10, side='left')

        # create a vertical scrollbar for the treeview
        vsb = ttk.Scrollbar(frame_results_of_historic_prices, orient="vertical",
                            command=historic_prices_tree.yview)
        vsb.pack(side='left', fill='y')

        # configure the treeview to use the scrollbar
        historic_prices_tree.configure(yscrollcommand=vsb.set)

        # set the height of the treeviw to show more rows
        historic_prices_tree['height'] = 20

        def export_to_excel(historic_prices_tree):
            wb = openpyxl.Workbook()
            ws = wb.active

            # write column headings
            for col, heading in enumerate(historic_prices_tree["columns"]):
                ws.cell(row=1, column=col+1,
                        value=historic_prices_tree.heading(heading)["text"])

            # write data
            for row, item in enumerate(historic_prices_tree.get_children()):
                for col, value in enumerate(historic_prices_tree.item(item)["values"]):
                    ws.cell(row=row+2, column=col+1, value=value)

            # save the workbook
            wb.save(ticker_symbol+"_treeview_data.xlsx")
            print("Exported to Excel")

        export_button = tk.Button(frame_results_of_historic_prices, text="Export to Excel",
                                  command=lambda: export_to_excel(historic_prices_tree))
        export_button.pack(side='right', padx=10, pady=10)

        frame_results_of_historic_prices.mainloop()

    # Ticker entry section
    label_title_ticker = customtkinter.CTkLabel(
        master=frame_historic_prices, text='Historic Prices', font=("Arial", 24))
    label_title_ticker.grid(row=1, column=1, columnspan=2)

    label_ticker_entry = customtkinter.CTkLabel(
        master=frame_historic_prices, text='Enter the stock ticker : ', font=("Arial", 18))
    label_ticker_entry.grid(row=3, column=3, sticky='W')

    entry_ticker_entry = customtkinter.CTkEntry(
        master=frame_historic_prices, width=200)
    entry_ticker_entry.grid(row=3, column=4, sticky='W')
    entry_ticker_entry.focus()

    period_textbox = customtkinter.CTkTextbox(
        master=frame_historic_prices, width=50, height=20)
    period_textbox.grid(row=4, column=4, sticky='W')

    button_search_historic_prices = customtkinter.CTkButton(
        master=frame_historic_prices, text='Search', command=results_of_historic_prices)
    button_search_historic_prices.grid(row=5, column=3, sticky='W')

    frame_historic_prices.mainloop()


def calculation_of_shares_to_buy():
    print('Calculation of shares to buy selected')

    '''
    - find the stock you want to buy
    - retreive its price per shares
    - input budget
    - input commissions
    - ...
    '''


def building_a_portfolio():
    print('Building a portfolio was selected')
    '''
    - Select new portfolio or previoulsy made
    
    - Forms
        - input cash
        - input propotion of each type of securities
            - Bonds
            - CAN stocks
            - US stocks
            - INT stocks
            - Alternatives
            - Cash
            - Fixed income
        - input target volatility
        - input target beta
        - input risk-free rate, and tresury yield
        - input age
        - input target retirement age
        - input needs of cash
        - input horizon
        - ...
        
        *
        - stock that would automatically be selected
            - select strategy
                - dividend
                - Growth
                - value
                - low vol
        - stock picked by us
        *
    
    - Calculations
        - each stock volatility, beta, ...
        - portfolio expected return
        - portfolio volatility
        - portfolio beta
        - *stock finder
        - ...
        
    - Output 
        - proportion for each type of security
        - proportion of each stocks to be invested
        - total cash used and total remaining
        - portfolio return
        - portfolio volatility
        - portfolio beta
        - graph
        - ...
    
    - make it possible to set the starting date, to keep track of the investments
    - try to implement simulations 
    - ...
    
    '''


mainframe = customtkinter.CTkFrame(master=mainroot)
mainframe._corner_radius = 40
mainframe.pack(pady=20, padx=60, fill='both', expand=True)

title_mainframe = customtkinter.CTkLabel(
    master=mainframe, text='Financial Tools', font=('Arial', 28))
title_mainframe.pack(pady=12, padx=10)

button_historic_price = customtkinter.CTkButton(
    master=mainframe, text='Historic prices', command=historic_prices)
button_historic_price.pack(pady=12, padx=10)

button_building_portfolio = customtkinter.CTkButton(
    master=mainframe, text='Building your portfolio (soon)', command=building_a_portfolio)
button_building_portfolio.pack(pady=12, padx=10)

button_calculation_of_shares_to_buy = customtkinter.CTkButton(
    master=mainframe, text='Calcul the number of share to buy (soon)', command=calculation_of_shares_to_buy)
button_calculation_of_shares_to_buy.pack(pady=12, padx=10)


mainroot.mainloop()
