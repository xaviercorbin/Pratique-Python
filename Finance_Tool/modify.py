import sqlite3
import customtkinter
import tkinter as tk
from tkinter import ttk

customtkinter.set_default_color_theme("dark-blue")
root = tk.Tk()
style = ttk.Style()
style.theme_use("clam")

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("SELECT * FROM User_Investment_Policy_Statement")
data = c.fetchall()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Calculating the x and y position to center the window
x = int(screen_width/2 - 500/2)
y = int(screen_height/2 - 350/2)

cols = ('name', 'money_to_invest', 'target_volatility', 'beta', 'age', 'investment_horizon', 'money_needed')
treeview = ttk.Treeview(master=root, columns=cols, show='headings')
for col in cols:
    treeview.heading(col, text=col.title())

for row in data:
    treeview.insert('', 'end', values=row)

treeview.grid(row=1, column=0, columnspan=6)

# Set the width of the treeview widget
treeview.column("#0", width=0)
for col in cols:
    treeview.column(col, width=200)

# Calculate the required width of the treeview widget
treeview_width = sum(treeview.column(col, width=None) for col in cols)

root.geometry(f"{treeview_width}x400+{x-350}+{y-100}")
root.title("Gestionnaire de la DataBase : users.db")

customtkinter.CTkLabel(master=root, text='Name').grid(row=2, column=0, sticky='w', padx=10)
name_entry = customtkinter.CTkEntry(master=root, width=200)
name_entry.grid(row=2, column=1, sticky='w', padx=10)

customtkinter.CTkLabel(master=root, text='change target volatility').grid(row=3, column=0, sticky='w', padx=10)
target_volatility_entry = customtkinter.CTkEntry(master=root, width=200)
target_volatility_entry.grid(row=3, column=1, sticky='w', padx=10)




def Update_treeview():
    # Remove row from table
    treeview.delete(*treeview.get_children())
    # Get updated data from database
    c.execute("SELECT * FROM User_Investment_Policy_Statement")
    data = c.fetchall()
    # Insert updated data into treeview
    for row in data:
        treeview.insert('', 'end', values=row)

def close_program():
    conn.close()
    root.destroy()
    
customtkinter.set_default_color_theme("green")
close_button = customtkinter.CTkButton(master=root, text="Close the Program", command=close_program)
close_button.grid(row=6, column=0, pady=15, sticky='w', padx=10)
customtkinter.set_default_color_theme("dark-blue")

def change_volatility():
    target_volatility_to_change = target_volatility_entry.get()
    name = name_entry.get()

    c.execute("UPDATE User_Investment_Policy_Statement SET target_volatility=? WHERE name=?", (target_volatility_to_change, name))
    conn.commit()
    # Update the value in the treeview
    Update_treeview()

change_volatility_button = customtkinter.CTkButton(master=root, text="Change target volatility", command=change_volatility)
change_volatility_button.grid(row=4, column=0, sticky='w', padx=10)

root.mainloop()