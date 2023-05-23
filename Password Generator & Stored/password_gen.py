
'''
-------------------------------------------------------------
Password Generator and Storing It in a Database
-------------------------------------------------------------
'''
import random
import sqlite3
import string
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

# Creating the interface
ctk.set_appearance_mode('system')
ctk.set_default_color_theme('dark-blue')


class PasswordGeneratorApp:
    def __init__(self, root):
        self.create_widgets(root)

    def create_widgets(self, root):
        self.create_title(root)
        self.create_origin_entry(root)
        self.create_email_entry(root)
        self.create_username_entry(root)
        self.create_generate_button(root)
        self.create_password_display(root)
        self.create_select_button(root)

    def create_second_widget(self):
        Manage_Data = ctk.CTk()
        screen_width = Manage_Data.winfo_screenmmwidth()
        screen_height = Manage_Data.winfo_screenheight()

        x = int((screen_width / 2) - (480 / 2))
        y = int((screen_height / 2) - (600 / 2))
        Manage_Data.geometry(f"480x600+{x}+{y}")
        Manage_Data.grid_columnconfigure(1, weight=1)
        Manage_Data.title('Manage Data')
        

    def create_title(self, root):
        title_label = ctk.CTkLabel(
            root, text='Password Generator', font=('Arial', 24))
        title_label.grid(row=0, column=0, padx=10, pady=40, sticky='w')

    def create_origin_entry(self, root):
        origin_label = ctk.CTkLabel(root, text='Origin of your password:')
        origin_label.grid(row=2, column=0, padx=10, sticky='w')
        self.origin_entry = ctk.CTkEntry(root)
        self.origin_entry.grid(row=2, column=1, pady=5, sticky='w')

    def create_email_entry(self, root):
        email_label = ctk.CTkLabel(root, text='Email:')
        email_label.grid(row=3, column=0, padx=10, sticky='w')
        self.email_entry = ctk.CTkEntry(root)
        self.email_entry.grid(row=3, column=1, pady=5, sticky='w')

    def create_username_entry(self, root):
        username_label = ctk.CTkLabel(root, text='Username:')
        username_label.grid(row=4, column=0, padx=10, sticky='w')
        self.username_entry = ctk.CTkEntry(root)
        self.username_entry.grid(row=4, column=1, pady=5, sticky='w')

    def create_generate_button(self, root):
        generate_button = ctk.CTkButton(
            root, text='Generate a Password', command=self.generate_password)
        generate_button.grid(row=6, column=1, pady=20, sticky='w')

    def create_password_display(self, root):
        password_label = ctk.CTkLabel(root, text='Generated Password:')
        password_label.grid(row=8, column=0, padx=10, sticky='w')
        self.password_textbox = ctk.CTkTextbox(root)
        self.password_textbox.grid(row=8, column=1, pady=5, sticky='w')

    def generate_password(self):
        alphabet = string.ascii_letters
        number = string.digits
        special_character = string.punctuation

        password = random.sample(
            alphabet, 7) + random.sample(number, 3) + random.sample(special_character, 3)
        random.shuffle(password)
        password = ''.join(password)

        self.update_password_display(password)

    def update_password_display(self, password):
        self.password_textbox.delete('1.0', 'end')
        self.password_textbox.insert('end', password)
        print('The Generated Password Was : ' + password)

    def create_select_button(self, root):
        select_button = ctk.CTkButton(
            root, text='Select', command=self.store_password)
        select_button.grid(row=10, column=1, pady=20, sticky='w')

    def manage_button(self, root):
        manage_button = ctk.CTkButton(
            root, text='Manage Data', command=self.manage_Password_Database)
        select_button.grid(row=10, column=1, pady=20, sticky='w')

    def store_password(self):
        origin = self.origin_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_textbox.get('1.0', 'end').strip()

        if origin and email and username and password:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS Password
                        (origin TEXT, email TEXT, username TEXT, password TEXT)''')
            c.execute("INSERT INTO Password VALUES (?, ?, ?, ?)",
                      (origin, email, username, password))
            conn.commit()
            conn.close()
            print('The saved password was :' + password)
        else:
            print("Please fill all the fields and generate a password.")
            # messagebox('ERROR', 'Please fill all the fields and generate a password.')

    def manage_Password_Database(self, Manage_Data):
        x = 2


if __name__ == "__main__":
    root = ctk.CTk()
    screen_width = root.winfo_screenmmwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (480 / 2))
    y = int((screen_height / 2) - (600 / 2))
    root.geometry(f"480x600+{x}+{y}")
    root.grid_columnconfigure(1, weight=1)
    root.title('Password Generator')

    password_generator_app = PasswordGeneratorApp(root)

    root.mainloop()
