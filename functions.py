import pandas as pd

def calculate_income(transactions):
    """Calculate total income from transactions."""
    return sum(t["amount"] for t in transactions if t["type"] == "Income")

def calculate_expenses(transactions):
    """Calculate total expenses from transactions."""
    return sum(t["amount"] for t in transactions if t["type"] == "Expense")

def calculate_balance(transactions):
    """Calculate balance (income - expenses)."""
    total_income = calculate_income(transactions)
    total_expenses = calculate_expenses(transactions)
    return total_income - total_expenses

def get_summary_dataframe(transactions):
    """Get a dataframe for summary visualization."""
    total_income = calculate_income(transactions)
    total_expenses = calculate_expenses(transactions)
    
    df = pd.DataFrame({
        "Category": ["Income", "Expenses"],
        "Amount": [total_income, total_expenses]
    })
    return df
