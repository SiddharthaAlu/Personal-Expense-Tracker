import streamlit as st
import pandas as pd
from functions import *
import datetime

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global styles for a fresh, modern appearance
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #eef4ff 0%, #ffffff 100%) !important;
}
.stApp {
    color-scheme: light;
}
div[data-testid="stSidebar"] {
    background: #1f3a93;
    color: white;
    padding: 20px 16px 10px 16px;
}
.css-1d391kg {
    background-color: rgba(255,255,255,0.75);
}
.stSidebar .css-15tx938 {
    background: transparent;
}
.stButton > button {
    background-color: #0066cc !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}
.stButton > button:hover {
    background-color: #0054a6 !important;
}
.stDivider {
    margin: 1.5rem 0;
}
.css-1kyxreq {
    border-radius: 20px;
}
.css-18e3th9 {
    padding: 2rem 2rem 2rem 2rem;
    background: rgba(255, 255, 255, 0.92);
    box-shadow: 0 20px 50px rgba(0,0,0,0.08);
    border-radius: 24px;
}
</style>
""", unsafe_allow_html=True)

# Store current page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Initialize transactions list
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Convert existing string dates to date objects
for t in st.session_state.transactions:
    if isinstance(t["date"], str):
        try:
            t["date"] = datetime.datetime.strptime(t["date"], "%Y-%m-%d").date()
        except ValueError:
            pass  # leave as is if can't parse

# Sidebar navigation
st.sidebar.title("Expense Tracker")
st.sidebar.markdown("#### Smart budgeting made simple")

if st.sidebar.button("Home"):
    st.session_state.page = "Home"

if st.sidebar.button("Add Transaction"):
    st.session_state.page = "Add Transaction"

if st.sidebar.button("View Transactions"):
    st.session_state.page = "View Transactions"

if st.sidebar.button("Summary"):
    st.session_state.page = "Summary"

page = st.session_state.page

if page == "Home":
    st.markdown(
        "<div style='border-radius: 30px; padding: 40px; background: linear-gradient(135deg, #1d8cf8 0%, #3358ff 100%); color: white;'>"
        "<h1 style='margin: 0; font-size: 3rem; text-align:center;'>Expense Tracker</h1>"
        "<p style='text-align:center; font-size:1.1rem; margin-top: 0.5rem; opacity:0.92;'>Track spending, visualize your cash flow, and stay ahead of your budget.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    total_income = calculate_income(st.session_state.transactions)
    total_expenses = calculate_expenses(st.session_state.transactions)
    balance = calculate_balance(st.session_state.transactions)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:,.2f}", delta="+income")
    col2.metric("Total Expenses", f"₹{total_expenses:,.2f}", delta="-expenses")
    col3.metric("Balance", f"₹{balance:,.2f}", delta="current")

    st.markdown("### Welcome")
    st.write(
        "This Expense Tracker helps you manage income and spending with a clean and modern interface. "
        "Use the sidebar to add transactions, review your history, and view a financial summary."
    )

    st.markdown("#### Features")
    st.markdown(
        "- Beautiful summary cards and charts\n"
        "- Easy transaction entry form\n"
        "- Clear transaction history table\n"
        "- Balance and expense breakdown visualization"
    )

    if st.session_state.transactions:
        st.markdown("### Recent Transactions")
        recent_df = pd.DataFrame(st.session_state.transactions[-5:]).rename(columns={"amount": "Amount (₹)"})
        def format_date(d):
            if hasattr(d, 'strftime'):
                return d.strftime("%d/%m/%Y")
            elif isinstance(d, str):
                try:
                    return pd.to_datetime(d).strftime("%d/%m/%Y")
                except:
                    return d
            else:
                return str(d)
        recent_df["date"] = recent_df["date"].apply(format_date)
        st.dataframe(recent_df)

elif page == "Add Transaction":
    st.markdown("<h2 style='color:#1d3a8a;'>Add a new transaction</h2>", unsafe_allow_html=True)
    st.write("Enter your income or expense details below to keep your budget up to date.")

    with st.form("add_transaction", clear_on_submit=True):
        left, right = st.columns([2, 1])
        with left:
            transaction_type = st.selectbox("Transaction Type", ["Income", "Expense"])
            category = st.text_input("Category / Source")
            description = st.text_area("Description", height=120)
        with right:
            amount_input = st.text_input("Amount (₹)", value="", placeholder="0.00")
            date = st.date_input("Date")
            submitted = st.form_submit_button("Add Transaction")

        if submitted:
            try:
                amount = float(amount_input)
            except ValueError:
                amount = -1

            if amount > 0:
                transaction = {
                    "type": transaction_type,
                    "category": category or "General",
                    "amount": amount,
                    "date": date,
                    "description": description,
                }
                st.session_state.transactions.append(transaction)
                st.success("Transaction added successfully.")
            else:
                st.error("Please enter a valid amount greater than zero.")

elif page == "View Transactions":
    st.markdown("<h2 style='color:#1d3a8a;'>Transaction History</h2>", unsafe_allow_html=True)
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions).rename(columns={"amount": "Amount (₹)"})
        def format_date(d):
            if hasattr(d, 'strftime'):
                return d.strftime("%d/%m/%Y")
            elif isinstance(d, str):
                try:
                    return pd.to_datetime(d).strftime("%d/%m/%Y")
                except:
                    return d
            else:
                return str(d)
        df["date"] = df["date"].apply(format_date)
        df["Indicator"] = df["type"].apply(lambda x: "🔵 Income" if x == "Income" else "🔴 Expense")
        st.dataframe(df)
    else:
        st.warning("No transactions have been added yet. Go to Add Transaction to get started.")

elif page == "Summary":
    st.markdown("<h2 style='color:#1d3a8a;'>Summary</h2>", unsafe_allow_html=True)
    if st.session_state.transactions:
        total_income = calculate_income(st.session_state.transactions)
        total_expenses = calculate_expenses(st.session_state.transactions)
        balance = calculate_balance(st.session_state.transactions)

        col1, col2, col3 = st.columns(3)
        col1.metric("Income", f"₹{total_income:,.2f}", delta="+income")
        col2.metric("Expenses", f"₹{total_expenses:,.2f}", delta="-expenses")
        col3.metric("Balance", f"₹{balance:,.2f}", delta="current")

        df = get_summary_dataframe(st.session_state.transactions)
        st.markdown("### Category Breakdown")
        st.bar_chart(df.set_index("Category"))

        with st.expander("View detailed transaction breakdown"):
            detailed_df = pd.DataFrame(st.session_state.transactions).rename(columns={"amount": "Amount (₹)"})
            def format_date(d):
                if hasattr(d, 'strftime'):
                    return d.strftime("%d/%m/%Y")
                elif isinstance(d, str):
                    try:
                        return pd.to_datetime(d).strftime("%d/%m/%Y")
                    except:
                        return d
                else:
                    return str(d)
            detailed_df["date"] = detailed_df["date"].apply(format_date)
            st.dataframe(detailed_df)
    else:
        st.info("No transactions yet. Add some entries to generate your summary.")
