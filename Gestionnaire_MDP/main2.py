import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from cryptography.fernet import Fernet
import json
import pyperclip
import secrets
import string

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Mots de Passe")
        self.pw_data = self.load_passwords()
        
        self.setup_ui()

    def load_or_create_key(self):
        try:
            with open('key.key', 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open('key.key', 'wb') as key_file:
                key_file.write(key)
            return key

    def encrypt_data(self, data):
        key = self.load_or_create_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        with open('passwords.enc', 'wb') as file:
            file.write(encrypted_data)

    def decrypt_data(self, key):
        fernet = Fernet(key)
        try:
            with open('passwords.enc', 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data).decode()
            return json.loads(decrypted_data)
        except Exception as e:
            return {}

    def load_passwords(self):
        key = self.load_or_create_key()
        return self.decrypt_data(key)

    def update_password_file(self):
        self.encrypt_data(json.dumps(self.pw_data))

    def add_or_update_entry(self, site, username, password):
        if not password:  # Generate a secure password if none is provided
            password = self.generate_secure_password()
        self.pw_data[site] = {'username': username, 'password': password}
        self.update_password_file()
        messagebox.showinfo("Succès", f"Entrée {'ajoutée' if username else 'mise à jour'} pour {site}.")
        self.refresh_treeview()

    def generate_secure_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for i in range(length))

    def setup_ui(self):
        self.tree = ttk.Treeview(self.root)
        self.tree['columns'] = ('Site', 'Utilisateur')
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Site", anchor=tk.W, width=120)
        self.tree.column("Utilisateur", anchor=tk.W, width=120)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.root.rowconfigure(i, weight=0)
            self.root.columnconfigure(i, weight=1)

        
        self.tree.heading("Site", text="Site", anchor=tk.W)
        self.tree.heading("Utilisateur", text="Utilisateur", anchor=tk.W)

        self.tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.site_label = tk.Label(self.root, text="Site:")
        self.site_entry = tk.Entry(self.root)
        self.user_label = tk.Label(self.root, text="Utilisateur:")
        self.user_entry = tk.Entry(self.root)
        self.pass_label = tk.Label(self.root, text="Mot de Passe:")
        self.pass_entry = tk.Entry(self.root, show="*")
        
        self.add_update_button = tk.Button(self.root, text="Ajouter/Mettre à jour", command=self.add_update)
        self.get_button = tk.Button(self.root, text="Récupérer", command=self.get_password)

        self.site_label.grid(row=1, column=0, padx=10, pady=10)
        self.site_entry.grid(row=1, column=1, padx=10, pady=10)
        self.user_label.grid(row=2, column=0, padx=10, pady=10)
        self.user_entry.grid(row=2, column=1, padx=10, pady=10)
        self.pass_label.grid(row=3, column=0, padx=10, pady=10)
        self.pass_entry.grid(row=3, column=1, padx=10, pady=10)
        
        self.add_update_button.grid(row=4, column=0, padx=10, pady=10)
        self.get_button.grid(row=4, column=1, padx=10, pady=10)

        self.refresh_treeview()

    def refresh_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for site, creds in self.pw_data.items():
            self.tree.insert('', 'end', values=(site, creds['username']))

    def add_update(self):
        site = self.site_entry.get()
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if site and username:
            self.add_or_update_entry(site, username, password)
            self.site_entry.delete(0, tk.END)
            self.user_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Le site et l'utilisateur sont requis.")

    def get_password(self):
        site = self.site_entry.get()
        if site in self.pw_data:
            entry = self.pw_data[site]
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, entry['username'])
            self.pass_entry.delete(0, tk.END)
            self.pass_entry.insert(0, entry['password'])
            messagebox.showinfo("Récupéré", f"Mot de passe pour {site} récupéré et affiché.")
            pyperclip.copy(entry['password'])  # Copie automatiquement le mot de passe dans le presse-papiers.
        else:
            messagebox.showerror("Erreur", "Site non trouvé.")
            self.user_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)


# Ajoutons un peu de code pour démarrer l'application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")  # Définit une taille initiale pour la fenêtre.
    app = PasswordManager(root)
    root.mainloop()
