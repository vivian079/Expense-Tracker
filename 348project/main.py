import sqlite3

conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        amount REAL
     )
''')

conn.commit()
conn.close()

def add_expense(date, category, amount):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO expenses (date, category, amount)
        VALUES (?, ?, ?)
    ''', (date, category, amount))
    
    conn.commit()
    conn.close()
    
def view_expenses():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    
    print("\nView Expenses")
    for expense in expenses:
        id, date, category, description, amount = expense
        print(f"ID: {id}, Date: {date}, Category: {category}, Amount: {amount}")
    
    conn.close()
    
def main_menu():
    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. Edit Expense")
        print("4. View Expenses")
        print("5. Calculate Totals")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            date = input("Enter the date (YYYY-MM-DD): ")
            category = input("Enter the category: ")
            amount = float(input("Enter the amount: "))
            
            add_expense(date, category, amount)
            
            print("Expense added successfully!")
        # elif choice == '2':

        # elif choice == '3':

        elif choice == '4':
            view_expenses()
        # elif choice == '5':
            
        elif choice == '6':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option")

if __name__ == "__main__":
    main_menu()