import tkinter as tk
from tkinter import ttk
from main import add_expense, delete_expense_orm, edit_expense_orm, view_expenses_orm, calculate_totals_orm, initialize_sqlite_database, initialize_sqlalchemy_database, Expense
from sqlalchemy.orm import sessionmaker

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x400")

        # Initialize SQLite and SQLAlchemy databases
        initialize_sqlite_database()
        engine = initialize_sqlalchemy_database()
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.create_gui()

    def create_gui(self):
        # Create tabs
        self.tabs = ttk.Notebook(self.root)
        self.add_expense_tab()
        self.view_expenses_tab()
        self.calculate_totals_tab()

        # Pack the tabs
        self.tabs.pack(expand=1, fill="both")

    def add_expense_tab(self):
        tab1 = ttk.Frame(self.tabs)
        self.tabs.add(tab1, text="Add Expense")

        # Add Expense form
        ttk.Label(tab1, text="Date (YYYY-MM-DD):").grid(column=0, row=0, padx=10, pady=10)
        self.date_entry = ttk.Entry(tab1)
        self.date_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(tab1, text="Category:").grid(column=0, row=1, padx=10, pady=10)
        # Static Category Drop-down List
        categories = ['Food', 'Travel', 'Education', 'Entertainment', 'Electricity', 'Household', 'Groceries']
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(tab1, textvariable=self.category_var, values=categories)
        self.category_dropdown.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(tab1, text="Amount:").grid(column=0, row=2, padx=10, pady=10)
        self.amount_entry = ttk.Entry(tab1)
        self.amount_entry.grid(column=1, row=2, padx=10, pady=10)

        ttk.Button(tab1, text="Add Expense", command=self.add_expense).grid(column=0, row=3, columnspan=2, pady=10)


    def view_expenses_tab(self):
        tab2 = ttk.Frame(self.tabs)
        self.tabs.add(tab2, text="View Expenses")

        # View Expenses listbox
        self.expenses_listbox = tk.Listbox(tab2, selectmode=tk.SINGLE, height=10, width=50)
        self.expenses_listbox.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        ttk.Button(tab2, text="Refresh", command=self.refresh_expenses).grid(column=0, row=1, columnspan=2, pady=10)
        ttk.Button(tab2, text="Delete Expense", command=self.delete_expense).grid(column=0, row=2, pady=10)
        ttk.Button(tab2, text="Edit Expense", command=self.edit_expense).grid(column=1, row=2, pady=10)

    def calculate_totals_tab(self):
        tab3 = ttk.Frame(self.tabs)
        self.tabs.add(tab3, text="Calculate Totals")

        # Calculate Totals label
        self.totals_label = ttk.Label(tab3, text="")
        self.totals_label.grid(column=0, row=0, pady=20)

        ttk.Button(tab3, text="Refresh", command=self.refresh_totals).grid(column=0, row=1, pady=10)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_var.get()
        amount = float(self.amount_entry.get())

        add_expense(date, category, amount)
        self.date_entry.delete(0, tk.END)
        self.category_var.set('')  # Reset category selection
        self.amount_entry.delete(0, tk.END)

    def refresh_expenses(self):
        self.expenses_listbox.delete(0, tk.END)
        expenses = view_expenses_orm(self.session)
        for expense in expenses:
            self.expenses_listbox.insert(tk.END, f"ID: {expense.id}, Date: {expense.date}, Category: {expense.category}, Amount: {expense.amount}")

    def delete_expense(self):
        selected_index = self.expenses_listbox.curselection()
        if selected_index:
            expense_info = self.expenses_listbox.get(selected_index)
            expense_id = int(expense_info.split(":")[1].split(",")[0].strip())
            delete_expense_orm(self.session, expense_id)
            self.refresh_expenses()

    def edit_expense(self):
        selected_index = self.expenses_listbox.curselection()
        if selected_index:
            expense_info = self.expenses_listbox.get(selected_index)
            expense_id = int(expense_info.split(":")[1].split(",")[0].strip())
            # Fetch existing data for the selected expense
            expense = self.session.query(Expense).filter_by(id=expense_id).first()
            if expense:
                edit_window = tk.Toplevel(self.root)
                edit_window.title("Edit Expense")

                ttk.Label(edit_window, text="New Date (YYYY-MM-DD):").grid(column=0, row=0, padx=10, pady=10)
                new_date_entry = ttk.Entry(edit_window)
                new_date_entry.insert(0, expense.date)
                new_date_entry.grid(column=1, row=0, padx=10, pady=10)

                ttk.Label(edit_window, text="New Category:").grid(column=0, row=1, padx=10, pady=10)
                new_category_entry = ttk.Entry(edit_window)
                new_category_entry.insert(0, expense.category)
                new_category_entry.grid(column=1, row=1, padx=10, pady=10)

                ttk.Label(edit_window, text="New Amount:").grid(column=0, row=2, padx=10, pady=10)
                new_amount_entry = ttk.Entry(edit_window)
                new_amount_entry.insert(0, expense.amount)
                new_amount_entry.grid(column=1, row=2, padx=10, pady=10)

                ttk.Button(edit_window, text="Save Changes", command=lambda: self.save_changes(expense_id, new_date_entry.get(), new_category_entry.get(), new_amount_entry.get())).grid(column=0, row=3, columnspan=2, pady=10)

    def get_categories(self):
        categories = [result[0] for result in self.session.query(Expense.category).distinct()]
        return categories

    def refresh_totals(self):
        total = calculate_totals_orm(self.session)
        self.totals_label.config(text=f"Total Expenses: {total}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
