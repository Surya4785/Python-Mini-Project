import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


DATA_FILE = "finance_data.json"


if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
else:
    data = {"income": [], "expenses": []}


def save_data():
    """Save the current data to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)


def add_income():
    """Add an income entry."""
    try:
        amount = float(income_amount_entry.get())
        source = income_source_entry.get()
        if not source:
            raise ValueError("Source cannot be empty.")
        data["income"].append({"source": source, "amount": amount})
        save_data()
        refresh_data()
        messagebox.showinfo("Success", "Income added successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def add_expense():
    """Add an expense entry."""
    try:
        amount = float(expense_amount_entry.get())
        category = expense_category_entry.get()
        if not category:
            raise ValueError("Category cannot be empty.")
        data["expenses"].append({"category": category, "amount": amount})
        save_data()
        refresh_data()
        messagebox.showinfo("Success", "Expense added successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def refresh_data():
    """Refresh the data displayed in the treeviews."""
    for item in income_tree.get_children():
        income_tree.delete(item)
    for income in data["income"]:
        income_tree.insert("", "end", values=(income["source"], f"${income['amount']:.2f}"))

    for item in expense_tree.get_children():
        expense_tree.delete(item)
    for expense in data["expenses"]:
        expense_tree.insert("", "end", values=(expense["category"], f"${expense['amount']:.2f}"))

    total_income = sum(i["amount"] for i in data["income"])
    total_expense = sum(e["amount"] for e in data["expenses"])
    balance = total_income - total_expense

    total_label.config(text=f"Total Income: ${total_income:.2f} | Total Expenses: ${total_expense:.2f} | Balance: ${balance:.2f}")



root = tk.Tk()
root.title("Self-Finance Manager")


income_frame = ttk.LabelFrame(root, text="Income")
income_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(income_frame, text="Source:").grid(row=0, column=0, padx=5, pady=5)
income_source_entry = ttk.Entry(income_frame)
income_source_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(income_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
income_amount_entry = ttk.Entry(income_frame)
income_amount_entry.grid(row=1, column=1, padx=5, pady=5)

add_income_button = ttk.Button(income_frame, text="Add Income", command=add_income)
add_income_button.grid(row=2, column=0, columnspan=2, pady=10)

income_tree = ttk.Treeview(income_frame, columns=("Source", "Amount"), show="headings")
income_tree.heading("Source", text="Source")
income_tree.heading("Amount", text="Amount")
income_tree.grid(row=3, column=0, columnspan=2, pady=10)


expense_frame = ttk.LabelFrame(root, text="Expenses")
expense_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

tk.Label(expense_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
expense_category_entry = ttk.Entry(expense_frame)
expense_category_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(expense_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
expense_amount_entry = ttk.Entry(expense_frame)
expense_amount_entry.grid(row=1, column=1, padx=5, pady=5)

add_expense_button = ttk.Button(expense_frame, text="Add Expense", command=add_expense)
add_expense_button.grid(row=2, column=0, columnspan=2, pady=10)

expense_tree = ttk.Treeview(expense_frame, columns=("Category", "Amount"), show="headings")
expense_tree.heading("Category", text="Category")
expense_tree.heading("Amount", text="Amount")
expense_tree.grid(row=3, column=0, columnspan=2, pady=10)

total_label = tk.Label(root, text="", font=("Arial", 12))
total_label.grid(row=1, column=0, columnspan=2, pady=10)

refresh_data()

root.mainloop()
