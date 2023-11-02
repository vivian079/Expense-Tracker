import tkinter as tk
from main import add_expense

def add_expense_button_clicked():
    date = date_entry.get()
    category = category_entry.get()
    amount = float(amount_entry.get())

    add_expense(date, category, amount)

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Expense Tracker")


date_label = tk.Label(root, text="Date:")
date_label.pack()

date_entry = tk.Entry(root)
date_entry.pack()

category_label = tk.Label(root, text="Category:")
category_label.pack()

category_entry = tk.Entry(root)
category_entry.pack()

amount_label = tk.Label(root, text="Amount:")
amount_label.pack()

amount_entry = tk.Entry(root)
amount_entry.pack()

add_button = tk.Button(root, text="Add Expense", command=add_expense_button_clicked)
add_button.pack()

root.mainloop()
