import os
import pickle
from tkinter import *

import customtkinter

# Créer l'interface
# Section pour mon "root"
customtkinter.set_appearance_mode('system')
customtkinter.set_default_color_theme('dark-blue')
root = customtkinter.CTk()
root.geometry('800x800')
root.title('My To Do List')

# Test
# Section pour le frame (par dessus le root, pour essayer de faire plus moderne)
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=40, fill='both', expand=True)


# Vérifier si un fichier contenant les tasks existe, et les charger si le fichier existe
if os.path.isfile('tasks.pkl'):
    with open('tasks.pkl', 'rb') as f:
        tasks = pickle.load(f)
else:
    tasks = []

task_listbox = Listbox(frame, bg='lightgrey', font=(
    'Arial', 20), width=45, height=25)
for task in tasks:
    task_listbox.insert(END, task)
task_listbox.pack(padx=10, pady=10)


# Interface pour ajouter une tâche
# Variable Globale
entry_add_task = None
add_task_window = None


def open_add_task():
    global entry_add_task, add_task_window
    # Créer la fenêtre
    add_task_window = Toplevel(root)
    add_task_window.title('Ajouter une tâche')
    add_task_window.geometry('800x50')

    # Créer le entry
    entry_add_task = customtkinter.CTkEntry(master=add_task_window)
    entry_add_task.pack(expand=True, fill='both')
    entry_add_task.focus()

    add_task_window.bind('<Return>', add_task)


# Ajouter une tâche
def add_task(event=None):
    global entry_add_task, add_task_window
    task = entry_add_task.get()
    if task != "":
        task_listbox.insert(END, task)
        tasks.append(task)
        entry_add_task.delete(0, END)
        save_task()
        add_task_window.destroy()


# Enleever une tâche
def remove_task():
    if task_listbox.curselection():
        task_index = task_listbox.curselection()[0]
        task_listbox.delete(ANCHOR)
        tasks.pop(task_index)
        save_task()

# Enregistrer les tâches


def save_task():
    with open('tasks.pkl', 'wb') as f:
        pickle.dump(list(task_listbox.get(0, END)), f)

# Fermer le programme


def close_program(event=None):
    root.destroy()


# Créer un bouton pour ouvrir une interface pour ajouter une tâche
add_task_button = Button(frame, text='Ajouter une tâche', bg='lightgrey', font=(
    'Arial', 20), width=25, height=3, command=open_add_task)
add_task_button.pack(padx=5, pady=5)

# Bouton pour suprimer une tâche
button_remove_task = Button(
    root, text="Remove Task", font=("Arial", 16), command=remove_task)
button_remove_task.pack(padx=5, pady=5)

# Associer la touche escape pour femrer le programe
root.bind('<Escape>', close_program)


root.mainloop()
