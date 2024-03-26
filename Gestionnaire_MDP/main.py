import tkinter as tk
from tkinter import simpledialog
from cryptography.fernet import Fernet
import json
import pyperclip
import secrets
import string

# Générer ou charger une clé de chiffrement
def load_or_create_key():
    try:
        with open('key.key', 'rb') as key_file:
            key = key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)
    return key

# Chiffrement des données
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    with open('passwords.enc', 'wb') as file:
        file.write(encrypted_data)

# Déchiffrement des données
def decrypt_data(key):
    fernet = Fernet(key)
    try:
        with open('passwords.enc', 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return json.loads(decrypted_data)
    except FileNotFoundError:
        return {}

# Fonction pour copier dans le presse-papiers
def copy_to_clipboard(data):
    pyperclip.copy(data)
    print("Copié dans le presse-papiers.")

# Générer un mot de passe sécurisé
def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_password = ''.join(secrets.choice(characters) for i in range(length))
    return secure_password

def gui():
    root = tk.Tk()
    root.title("Gestionnaire de Mots de Passe")

    def unlock():
        key = load_or_create_key()
        pw_data = decrypt_data(key)
        
        def add_entry():
            site = simpledialog.askstring("Ajouter", "Nom du site:")
            username = simpledialog.askstring("Ajouter", "Nom d'utilisateur:")
            password = simpledialog.askstring("Ajouter", "Mot de passe (laisser vide pour générer):")
            if not password:
                password = generate_secure_password()
            pw_data[site] = {'username': username, 'password': password}
            encrypt_data(json.dumps(pw_data), key)
            print(f"Entrée ajoutée pour {site}.")
        
        def get_entry():
            site = simpledialog.askstring("Récupérer", "Nom du site:")
            if site in pw_data:
                entry = pw_data[site]
                print(f"Site: {site}, Utilisateur: {entry['username']}, Mot de passe: [CACHÉ]")
                copy_to_clipboard(entry['password'])
            else:
                print("Site non trouvé.")
        
        add_btn = tk.Button(root, text="Ajouter Entrée", command=add_entry)
        get_btn = tk.Button(root, text="Récupérer Entrée", command=get_entry)
        add_btn.pack(pady=5)
        get_btn.pack(pady=5)

    unlock_btn = tk.Button(root, text="Déverrouiller Gestionnaire", command=unlock)
    unlock_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    gui()
