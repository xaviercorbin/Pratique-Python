import os
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, ttk

import customtkinter
import openpyxl
import pandas as pd

customtkinter.set_appearance_mode('system')
customtkinter.set_default_color_theme('dark-blue')
mainroot = customtkinter.CTk()
screen_width = mainroot.winfo_screenwidth()
screen_height = mainroot.winfo_screenheight()

# Pour essayer de centrer la fenêtre au centre
x = int(screen_width/2 - 500/2)
y = int(screen_height/2 - 350/2)
mainroot.geometry(f"500x400+{x}+{y}")
mainroot.title("Games")


def first_game():
    # Création du fichier
    print('x')

mainframe = customtkinter.CTkFrame(master=mainroot)
mainframe._corner_radius = 40
mainframe.pack(pady=20, padx=60, fill='both', expand=True)

button_first_game = customtkinter.CTkButton(master=mainframe, text="First Game", command=first_game)
button_first_game.pack(pady=12, padx=10)


mainroot.mainloop()