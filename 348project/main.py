import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import datetime

# SQLite Initialization
def initialize_sqlite_database():
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
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON expenses (date);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON expenses (category);')
    conn.commit()
    conn.close()

# SQLAlchemy Initialization
Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    category = Column(String)
    amount = Column(Float)

def initialize_sqlalchemy_database():
    engine = create_engine('sqlite:///expense_tracker.db', echo=True)
    Base.metadata.create_all(engine)
    return engine

# Prepared Statements for SQLite
def add_expense(date, category, amount):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    query = 'INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)'
    cursor.execute(query, (date, category, amount))
    conn.commit()
    conn.close()

# ORM with SQLAlchemy
def delete_expense_orm(session, expense_id):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()

def edit_expense_orm(session, expense_id, date, category, amount):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        expense.date = date
        expense.category = category
        expense.amount = amount
        session.commit()

def view_expenses_orm(session):
    expenses = session.query(Expense).all()
    return expenses

def calculate_totals_orm(session):
    total = session.query(func.sum(Expense.amount)).scalar()
    return total

# Functions
def main_menu():
    # Initialize SQLite and SQLAlchemy databases
    initialize_sqlite_database()
    engine = initialize_sqlalchemy_database()
    Session = sessionmaker(bind=engine)
    session = Session()

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

        elif choice == '2':
            expense_id = input("Enter the ID of the expense to delete: ")
            delete_expense_orm(session, expense_id)
            print("Expense deleted successfully!")

        elif choice == '3':
            expense_id = input("Enter the ID of the expense to edit: ")
            date = input("Enter the new date (YYYY-MM-DD): ")
            category = input("Enter the new category: ")
            amount = float(input("Enter the new amount: "))
            edit_expense_orm(session, expense_id, date, category, amount)
            print("Expense edited successfully!")

        elif choice == '4':
            expenses = view_expenses_orm(session)
            print("\nView Expenses (Using ORM)")
            for expense in expenses:
                print(f"ID: {expense.id}, Date: {expense.date}, Category: {expense.category}, Amount: {expense.amount}")

        elif choice == '5':
            total = calculate_totals_orm(session)
            print(f"\nTotal Expenses: {total}")

        elif choice == '6':
            print("Exiting Expense Tracker. Goodbye!")
            session.close()
            break

        else:
            print("Invalid choice. Please choose a valid option")

if __name__ == "__main__":
    main_menu()
