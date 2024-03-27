import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet

# Générer une clé. Dans une application réelle, vous devez sauvegarder cette clé de manière sécurisée.
# Pour simplifier, nous la générons à chaque fois ici. Dans la pratique, chargez cette clé depuis un endroit sûr.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_password(password: str) -> bytes:
    """Chiffre le mot de passe."""
    return cipher_suite.encrypt(password.encode('utf-8'))

def decrypt_password(encrypted_password: bytes) -> str:
    """Déchiffre le mot de passe."""
    return cipher_suite.decrypt(encrypted_password).decode('utf-8')

# Simule un stockage de mots de passe. Dans une application réelle, cela serait remplacé par un stockage sécurisé.
passwords = {}

def add_password():
    """Ajoute un nouveau mot de passe après l'avoir chiffré."""
    service = simpledialog.askstring("Service", "Entrez le nom du service:")
    if service in passwords:
        messagebox.showerror("Erreur", "Ce service est déjà enregistré.")
        return
    pwd = simpledialog.askstring("Mot de Passe", "Entrez le mot de passe:", show='*')
    if pwd:
        encrypted_pwd = encrypt_password(pwd)
        passwords[service] = encrypted_pwd
        update_password_list()

def update_password_list():
    """Met à jour la liste des mots de passe affichés."""
    password_list.delete(0, tk.END)
    for service in passwords:
        password_list.insert(tk.END, service)

# Initialisation de l'interface Tkinter
root = tk.Tk()
root.title("Gestionnaire de Mots de Passe")

# Liste pour afficher les services enregistrés
password_list = tk.Listbox(root)
password_list.pack(pady=20)

# Bouton pour ajouter un nouveau mot de passe
add_button = tk.Button(root, text="Ajouter Mot de Passe", command=add_password)
add_button.pack(pady=10)

update_password_list()  # Mettre à jour la liste pour la première fois

root.mainloop()
