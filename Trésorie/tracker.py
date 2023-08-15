import tkinter as tk
from tkinter import ttk
import sqlite3

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker App")

        self.create_widgets()

    def create_widgets(self):
        self.expense_amount = tk.DoubleVar()
        self.budget_amount = tk.DoubleVar()  # New budget entry variable
        self.categories = ["Alimentation", "Logement", "Transport", "Divertissement"]
        self.selected_category = tk.StringVar(value=self.categories)

        tk.Label(self.root, text="Montant de la dépense :").pack(pady=10)
        self.amount_entry = tk.Entry(self.root, textvariable=self.expense_amount)
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Catégorie :").pack()
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.selected_category, values=self.categories)
        self.category_dropdown.pack(pady=5)

        tk.Label(self.root, text="Budget :").pack()  # New budget label
        self.budget_entry = tk.Entry(self.root, textvariable=self.budget_amount)  # New budget entry
        self.budget_entry.pack(pady=5)  # New budget entry

        self.add_button = tk.Button(self.root, text="Ajouter la transaction", command=self.add_transaction)
        self.add_button.pack(pady=10)

        self.budget_label = tk.Label(self.root, text="", font=("Helvetica", 12, "bold"))
        self.budget_label.pack()

    def add_transaction(self):
        amount = self.expense_amount.get()
        category = self.selected_category.get()
        budget = self.budget_amount.get()  # Get the budget from the entry

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO transactions (amount, category, date, budget, expenses) VALUES (?, ?, DATETIME('now'), ?, ?)", (amount, category, budget, amount))
        conn.commit()

        conn.close()

        print(f"Transaction ajoutée : Montant = {amount}, Catégorie = {category}, Budget = {budget}")
        self.update_budget_display()

    def update_budget_display(self):
        selected_category = self.selected_category.get()
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("SELECT budget, expenses FROM transactions WHERE category=?", (selected_category,))
        row = cursor.fetchone()

        if row:
            budget, expenses = row
            remaining_budget = budget - expenses
            self.budget_label.config(text=f"Budget restant : {remaining_budget:.2f} €")

        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
