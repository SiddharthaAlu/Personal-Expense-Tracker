import pandas as pd
import streamlit as st

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
    """Build the two-row dataframe used by the income vs expenses chart."""
    total_income = calculate_income(transactions)
    total_expenses = calculate_expenses(transactions)
    
    df = pd.DataFrame({
        "Category": ["Income", "Expenses"],
        "Amount": [total_income, total_expenses]
    })
    return df

def calculate_savings_rate(transactions):
    """Calculate balance as a percentage of income, avoiding division by zero."""
    total_income = calculate_income(transactions)
    if total_income == 0:
        return 0
    balance = calculate_balance(transactions)
    return (balance / total_income) * 100

def get_transaction_count(transactions):
    """Get total number of transactions."""
    return len(transactions)

def get_average_transaction(transactions, transaction_type=None):
    """Return the average amount, optionally filtered by Income or Expense."""
    if transaction_type:
        filtered = [t["amount"] for t in transactions if t["type"] == transaction_type]
    else:
        filtered = [t["amount"] for t in transactions]
    
    if not filtered:
        return 0
    return sum(filtered) / len(filtered)

def get_highest_transaction(transactions, transaction_type=None):
    """Return the highest amount, optionally filtered by Income or Expense."""
    if transaction_type:
        filtered = [t for t in transactions if t["type"] == transaction_type]
    else:
        filtered = transactions
    
    if not filtered:
        return 0
    return max(t["amount"] for t in filtered)

def get_category_breakdown(transactions):
    """Group expense transactions by category for charts and top-category tables."""
    expenses = [t for t in transactions if t["type"] == "Expense"]
    if not expenses:
        return pd.DataFrame()
    
    df = pd.DataFrame(expenses)
    category_breakdown = df.groupby("category")["amount"].sum().reset_index()
    category_breakdown.columns = ["Category", "Amount"]
    return category_breakdown.sort_values("Amount", ascending=False)

def get_top_categories(transactions, limit=5):
    """Return the highest-spending categories after the category totals are sorted."""
    category_df = get_category_breakdown(transactions)
    return category_df.head(limit)


def format_date_value(value):
    """Convert dates from date objects or strings into DD/MM/YYYY display text."""
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, str):
        try:
            return pd.to_datetime(value).strftime("%d/%m/%Y")
        except Exception:
            return value
    return str(value)


def format_rupees(value):
    """Format a number as Indian currency with lakh/crore comma grouping."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return str(value)

    sign = "-" if amount < 0 else ""
    rupees, paise = f"{abs(amount):.2f}".split(".")

    # Keep the final three digits together, then group the remaining digits in pairs.
    if len(rupees) > 3:
        last_three = rupees[-3:]
        remaining = rupees[:-3]
        groups = []
        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        rupees = ",".join(groups + [last_three])

    return f"{sign}₹{rupees}.{paise}"


def parse_amount_input(value):
    """Clean currency symbols and commas from user input before converting to float."""
    cleaned_value = str(value).strip().replace("₹", "").replace(",", "").strip()
    if not cleaned_value:
        raise ValueError("Amount is empty")
    return float(cleaned_value)


def format_indian_number(value):
    """Format an amount for the input box without showing the currency symbol."""
    return format_rupees(value).replace("₹", "")


def format_amount_field():
    """Streamlit callback that prettifies the amount input after the user edits it."""
    raw_amount = st.session_state.get("amount_input", "")
    if not str(raw_amount).strip():
        return

    try:
        amount = parse_amount_input(raw_amount)
    except ValueError:
        return

    st.session_state.amount_input = format_indian_number(amount)


def add_transaction():
    """Validate the form fields and append a new transaction to session state."""
    try:
        amount = parse_amount_input(st.session_state.get("amount_input", ""))
    except ValueError:
        amount = -1

    if amount <= 0:
        st.session_state.transaction_message = ("error", "Please enter a valid amount greater than zero.")
        return

    # Store raw values in session state; display formatting happens only in the UI.
    transaction = {
        "type": st.session_state.transaction_type,
        "category": st.session_state.category_input,
        "amount": amount,
        "date": st.session_state.date_input,
        "description": st.session_state.description_input,
    }
    st.session_state.transactions.append(transaction)
    st.session_state.amount_input = ""
    st.session_state.description_input = ""
    st.session_state.transaction_message = ("success", "Transaction added successfully.")


def render_page_banner(title, subtitle, gradient, heading_level=2):
    """Render the colored page header used across the Streamlit pages."""
    heading_tag = "h1" if heading_level == 1 else "h2"
    st.markdown(
        f"<div style='border-radius: 24px; background: {gradient}; padding: 24px; margin-bottom: 18px; box-shadow: 0 12px 30px rgba(0,0,0,0.12);'>"
        f"<{heading_tag} style='margin: 0; color: white; text-align:center;'>{title}</{heading_tag}>"
        f"<p style='margin: 10px 0 0; color: rgba(255,255,255,0.95); font-size: 1rem; text-align:center;'>{subtitle}</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def get_category_options(transaction_type):
    """Return category choices based on whether the user is adding income or expense."""
    if transaction_type == "Income":
        return ["Salary", "Freelance", "Business", "Investment", "Other"]
    return ["Food", "Transportation", "Shopping", "Entertainment", "Rent", "Other"]


def style_transaction_amount(val):
    """Apply custom table styling to formatted currency values."""
    if isinstance(val, (int, float)) or str(val).strip().startswith("₹"):
        return "color: #d1fae5; font-weight: 700; text-align: left;"
    return ""


def sidebar_nav_button(label):
    """Render one sidebar navigation button and switch pages when it is clicked."""
    active = st.session_state.page == label
    button_type = "primary" if active else "secondary"

    if st.sidebar.button(
        label,
        key=f"sidebar_{label}",
        type=button_type,
        use_container_width=True
    ):
        st.session_state.page = label
        st.rerun()
