# imports.py

# Standard Library imports
import random
from datetime import date, datetime, timedelta
import sqlite3

# Third-party imports
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tkinter related imports
import tkinter as tk
from tkinter import ttk, IntVar, Canvas

print('Game started')

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

homepage = customtkinter.CTk()
homepage.title("TRADER")
homepage.attributes('-fullscreen', True)