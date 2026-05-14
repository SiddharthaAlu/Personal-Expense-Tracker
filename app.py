import streamlit as st
import pandas as pd
import altair as alt
import datetime
from functions import *

# Configure the Streamlit browser tab and page layout before rendering anything.
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS keeps the app styling consistent across Streamlit widgets.
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #eef4ff 0%, #ffffff 100%) !important;
}
.stApp {
    color-scheme: light dark;
}
div[data-testid="stSidebar"] {
    background: #1f3a93;
    color: white;
    padding: 20px 16px 10px 16px;
}
.stSidebar .stButton,
.stSidebar .stButton > button,
.stSidebar button {
    width: 100% !important;
    min-height: 52px !important;
}
.stSidebar .stButton > button,
.stSidebar button {
    background: linear-gradient(135deg, #93c5fd 0%, #2563eb 48%, #1e3a8a 100%) !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 18px;
    border: 1px solid rgba(191, 219, 254, 0.45) !important;
    box-shadow: 0 8px 20px rgba(30, 64, 175, 0.22);
    box-sizing: border-box;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    transition: background 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
}
.stSidebar .stButton > button:hover,
.stSidebar button:hover {
    background: linear-gradient(135deg, #bfdbfe 0%, #3b82f6 48%, #1d4ed8 100%) !important;
    box-shadow: 0 12px 26px rgba(30, 64, 175, 0.32);
    transform: translateY(-1px);
}
.stSidebar .stButton > button[kind="primary"],
.stSidebar button[kind="primary"] {
    background: linear-gradient(135deg, #86efac 0%, #22c55e 46%, #047857 100%) !important;
    color: white !important;
    border: 1px solid rgba(187, 247, 208, 0.55) !important;
    box-shadow: 0 10px 24px rgba(4, 120, 87, 0.32);
    transition: background 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
}
.stSidebar .stButton > button[kind="primary"]:hover,
.stSidebar button[kind="primary"]:hover {
    background: linear-gradient(135deg, #bbf7d0 0%, #34d399 42%, #065f46 100%) !important;
    box-shadow: 0 14px 30px rgba(4, 120, 87, 0.42);
    transform: translateY(-1px);
}
.stDivider {
    margin: 1.5rem 0;
}
.anchor-link,
[data-testid="stMarkdownContainer"] a[href^="#"],
[data-testid="stHeading"] a[href^="#"] {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stDataFrame"] [role="columnheader"],
[data-testid="stDataFrame"] [data-testid="stDataFrameResizableColumnHeader"] {
    background: #0f766e !important;
    color: #ffffff !important;
    font-weight: 800 !important;
}
[data-testid="stDataFrame"] [role="gridcell"] {
    text-align: left !important;
    justify-content: flex-start !important;
}
[data-testid="stDataFrame"] [role="gridcell"] > div,
[data-testid="stDataFrame"] [role="gridcell"] p,
[data-testid="stDataFrame"] [role="gridcell"] span {
    text-align: left !important;
    justify-content: flex-start !important;
}
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
[data-testid="stMetric"],
[data-testid="stMetric"] *,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] *,
[data-testid="stAlert"],
[data-testid="stAlert"] * {
    cursor: default !important;
}
button,
button *,
[role="button"],
[role="button"] *,
.stSidebar .stButton,
.stSidebar .stButton *,
.stSidebar button,
.stSidebar button *,
div[data-testid="stSidebar"] .stButton,
div[data-testid="stSidebar"] .stButton *,
div[data-testid="stSidebar"] button,
div[data-testid="stSidebar"] button * {
    cursor: pointer !important;
}
input,
textarea,
input *,
textarea * {
    cursor: text !important;
}
select,
select *,
div[data-testid="stSelectbox"],
div[data-testid="stSelectbox"] *,
div[data-baseweb="select"],
div[data-baseweb="select"] *,
ul[role="listbox"],
ul[role="listbox"] *,
[role="option"],
[role="option"] * {
    cursor: pointer !important;
}
div[data-testid="stSelectbox"] input,
div[data-baseweb="select"] input {
    cursor: pointer !important;
    caret-color: transparent !important;
    user-select: none !important;
}
div[data-testid="stButton"] button,
div[data-testid="stButton"] button *,
div[data-testid="stButton"] p {
    cursor: pointer !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] select,
div[data-testid="stDateInput"] input {
    background: #fff3ec !important;
    border: 1px solid #ffbc9a !important;
    color: #7f3f00 !important;
    border-radius: 14px !important;
    box-shadow: inset 0 1px 4px rgba(255, 149, 103, 0.18) !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stSelectbox"] select:focus,
div[data-testid="stDateInput"] input:focus {
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(255, 163, 109, 0.28) !important;
}

@media (prefers-color-scheme: dark), [data-theme="dark"] {
    body {
        background: linear-gradient(180deg, #0c1220 0%, #111827 100%) !important;
    }
    .stApp {
        color-scheme: dark;
    }
    div[data-testid="stSidebar"] {
        background: #111827;
        color: #d1d5db;
    }
    .stButton > button {
        background: linear-gradient(135deg, #60a5fa 0%, #2563eb 48%, #172554 100%) !important;
        color: white !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #93c5fd 0%, #3b82f6 48%, #1e3a8a 100%) !important;
    }
    .stSidebar .stButton > button[kind="primary"],
    .stSidebar button[kind="primary"] {
        background: linear-gradient(135deg, #5eead4 0%, #22c55e 46%, #064e3b 100%) !important;
        color: white !important;
        border: 1px solid rgba(45, 212, 191, 0.45) !important;
        box-shadow: 0 10px 24px rgba(20, 184, 166, 0.24);
    }
    .stSidebar .stButton > button[kind="primary"]:hover,
    .stSidebar button[kind="primary"]:hover {
        background: linear-gradient(135deg, #99f6e4 0%, #34d399 44%, #065f46 100%) !important;
        box-shadow: 0 14px 30px rgba(20, 184, 166, 0.32);
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stSelectbox"] select,
    div[data-testid="stDateInput"] input {
        background: #1f2937 !important;
        border: 1px solid #374151 !important;
        color: #f8fafc !important;
        box-shadow: inset 0 1px 4px rgba(15, 23, 42, 0.6) !important;
    }
    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stDateInput"] input::placeholder {
        color: #9ca3af !important;
    }
    [data-testid="stDataFrame"] [role="columnheader"],
    [data-testid="stDataFrame"] [data-testid="stDataFrameResizableColumnHeader"] {
        background: #14b8a6 !important;
        color: #ffffff !important;
    }
}
</style>
""", unsafe_allow_html=True)


# Session state stores page navigation and transactions between Streamlit reruns.
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "amount_input" not in st.session_state:
    st.session_state.amount_input = ""

# Normalize older saved date strings so the rest of the app can treat them as dates.
for t in st.session_state.transactions:
    if isinstance(t["date"], str):
        for date_format in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                t["date"] = datetime.datetime.strptime(t["date"], date_format).date()
                break
            except ValueError:
                pass

transactions = st.session_state.transactions

# Sidebar buttons control which page section is shown below.
st.sidebar.title("Expense Tracker")
st.sidebar.markdown("#### Smart budgeting made simple")

sidebar_nav_button("Home")
sidebar_nav_button("Add Transaction")
sidebar_nav_button("View Transactions")
sidebar_nav_button("Summary")

page = st.session_state.page

# Home page: quick totals, app overview, and the latest transaction.
if page == "Home":
    render_page_banner(
        "Expense Tracker",
        "Track spending, visualize your cash flow, and stay ahead of your budget.",
        "linear-gradient(135deg, #8cc9ff 0%, #12438a 100%)",
        heading_level=1,
    )

    st.markdown("---")

    total_income = calculate_income(transactions)
    total_expenses = calculate_expenses(transactions)
    balance = calculate_balance(transactions)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", format_rupees(total_income), delta="+income")
    col2.metric("Total Expenses", format_rupees(total_expenses), delta="-expenses")
    col3.metric("Balance", format_rupees(balance), delta="current")

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

    if transactions:
        # Show only the newest transaction as a compact snapshot on the home page.
        st.markdown("### Latest Transaction")
        recent_df = pd.DataFrame([transactions[-1]]).rename(columns={
            "type": "Type",
            "category": "Category",
            "amount": "Amount (₹)",
            "date": "Date",
            "description": "Description",
        })
        recent_df.index = range(1, len(recent_df) + 1)
        recent_df["Date"] = recent_df["Date"].apply(format_date_value)
        recent_df["Amount (₹)"] = recent_df["Amount (₹)"].apply(format_rupees)
        st.dataframe(recent_df)

# Add Transaction page: collects form values and saves them through add_transaction().
elif page == "Add Transaction":
    render_page_banner(
        "Add a new transaction",
        "Enter your income or expense details below to keep your budget up to date.",
        "linear-gradient(135deg, #ffb37d 0%, #ff7f6d 100%)",
    )

    transaction_type = st.selectbox("Transaction Type", ["Income", "Expense"], key="transaction_type")
    category_options = get_category_options(transaction_type)
    # Reset the selected category when switching between Income and Expense choices.
    if st.session_state.get("category_input") not in category_options:
        st.session_state.category_input = category_options[0]

    left, right = st.columns([2, 1])
    with left:
        st.selectbox("Category", category_options, key="category_input")
        st.text_area("Description", height=120, key="description_input")
    with right:
        st.text_input("Amount (₹)", key="amount_input", placeholder="0", on_change=format_amount_field)
        st.date_input("Date", key="date_input", format="DD/MM/YYYY")
        st.button("Add Transaction", on_click=add_transaction, use_container_width=True)

    # add_transaction stores success/error feedback here so it survives the rerun.
    message = st.session_state.pop("transaction_message", None)
    if message:
        message_type, message_text = message
        if message_type == "success":
            st.success(message_text)
        else:
            st.error(message_text)

# View Transactions page: formats, sorts, and styles the full transaction table.
elif page == "View Transactions":
    render_page_banner(
        "Transaction History",
        "Review your income and expense records with the same vibrant, easy-to-read table style.",
        "linear-gradient(135deg, #ffb37d 0%, #ff7f6d 100%)",
    )
    if transactions:
        df = pd.DataFrame(transactions).rename(columns={
            "type": "Type",
            "category": "Category",
            "amount": "Amount (₹)",
            "date": "Date",
            "description": "Description",
        })
        # Temporary sort columns keep sorting numeric/date-safe before display formatting.
        df["SortDate"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df["SortAmount"] = df["Amount (₹)"]

        sort_by = st.selectbox("Sort by", ["Date", "Amount (₹)"], key="transaction_sort_by")

        sort_key = "SortDate" if sort_by == "Date" else "SortAmount"
        ascending = False
        df = df.sort_values(sort_key, ascending=ascending).drop(columns=["SortDate", "SortAmount"])
        df.index = range(1, len(df) + 1)
        # Convert raw values into user-friendly text after sorting is complete.
        df["Date"] = df["Date"].apply(format_date_value)
        df["Amount (₹)"] = df["Amount (₹)"].apply(format_rupees)

        def style_type(val):
            if val == "Income":
                return "background-color: #064e3b; color: #bbf7d0; font-weight: 700;"
            return "background-color: #4c1d95; color: #ddd6fe; font-weight: 700;"

        styled_df = (
            df.style
              .applymap(style_type, subset=["Type"])
              .applymap(style_transaction_amount, subset=["Amount (₹)"])
              .set_properties(subset=["Amount (₹)"], **{"text-align": "left"})
              .set_properties(**{
                  "background-color": "#111827",
                  "color": "#e5e7eb",
                  "border": "1px solid #374151",
                  "font-family": "Arial, sans-serif",
                  "text-align": "left"
              })
              .set_table_styles([
                  {"selector": "th", "props": [("background-color", "#0f766e"), ("color", "#f8fafc"), ("font-size", "14px"), ("font-weight", "800"), ("border-bottom", "3px solid #5eead4"), ("text-align", "left")]},
                  {"selector": "td", "props": [("padding", "10px"), ("font-size", "13px"), ("border-bottom", "1px solid #374151"), ("text-align", "left")]},
                  {"selector": "tbody tr:nth-child(even) td", "props": [("background-color", "#1f2937")]},
                  {"selector": "tbody tr:hover td", "props": [("background-color", "#0f172a")]}
              ])
        )

        st.table(styled_df)
    else:
        st.warning("No transactions have been added yet. Go to Add Transaction to get started.")

# Summary page: calculates metrics and renders charts from the saved transactions.
elif page == "Summary":
    render_page_banner(
        "Summary",
        "Review your budget insights, income vs expenses, and spending trends in one place.",
        "linear-gradient(135deg, #ffb37d 0%, #ff7f6d 100%)",
    )
    if transactions:
        total_income = calculate_income(transactions)
        total_expenses = calculate_expenses(transactions)
        balance = calculate_balance(transactions)

        col1, col2, col3 = st.columns(3)
        col1.metric("Income", format_rupees(total_income), delta="+income")
        col2.metric("Expenses", format_rupees(total_expenses), delta="-expenses")
        col3.metric("Balance", format_rupees(balance), delta="current")

        st.markdown("---")
        st.markdown("### Analytics & Insights")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            savings_rate = calculate_savings_rate(transactions)
            st.metric("Savings Rate", f"{savings_rate:.1f}%")
        with col2:
            avg_expense = get_average_transaction(transactions, "Expense")
            st.metric("Avg Expense", format_rupees(avg_expense))
        with col3:
            avg_income = get_average_transaction(transactions, "Income")
            st.metric("Avg Income", format_rupees(avg_income))
        with col4:
            trans_count = get_transaction_count(transactions)
            st.metric("Total Transactions", trans_count)
        
        col1, col2 = st.columns(2)
        
        with col1:
            highest_expense = get_highest_transaction(transactions, "Expense")
            st.metric("Highest Expense", format_rupees(highest_expense))
        
        with col2:
            highest_income = get_highest_transaction(transactions, "Income")
            st.metric("Highest Income", format_rupees(highest_income))

        st.markdown("---")
        
        st.markdown("### Expense Breakdown by Category")
        category_df = get_category_breakdown(transactions)
        if not category_df.empty:
            # Tooltip labels are preformatted so charts show rupee values cleanly.
            category_chart_df = category_df.copy()
            category_chart_df["AmountLabel"] = category_chart_df["Amount"].apply(format_rupees)
            expense_chart = alt.Chart(category_chart_df).mark_bar(color="#1f77b4").encode(
                x=alt.X('Category:N', sort='-y', axis=alt.Axis(labelAngle=0, labelFontSize=12)),
                y=alt.Y('Amount:Q', axis=alt.Axis(title='Amount (₹)')),
                tooltip=[
                    alt.Tooltip('Category:N', title='Category'),
                    alt.Tooltip('AmountLabel:N', title='Amount')
                ]
            ).properties(width=700, height=400)
            st.altair_chart(expense_chart, use_container_width=True)

            st.markdown("### Top Spending Categories")
            top_cat = get_top_categories(transactions, 5).copy()
            top_cat.index = range(1, len(top_cat) + 1)
            top_cat["Amount"] = top_cat["Amount"].apply(format_rupees)
            st.dataframe(top_cat, use_container_width=True)
        else:
            st.info("No expense categories to display yet.")

        st.markdown("---")
        st.markdown("### Income vs Expenses")
        # The summary dataframe feeds the comparison chart and keeps labels consistent.
        df = get_summary_dataframe(transactions)
        df["AmountLabel"] = df["Amount"].apply(format_rupees)
        summary_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Category:N', sort=['Income', 'Expenses'], axis=alt.Axis(labelAngle=0, labelFontSize=12)),
            y=alt.Y('Amount:Q', axis=alt.Axis(title='Amount (₹)')),
            color=alt.Color('Category:N', scale=alt.Scale(domain=['Income', 'Expenses'], range=['#2ca02c', '#d62728'])),
            tooltip=[
                alt.Tooltip('Category:N', title='Category'),
                alt.Tooltip('AmountLabel:N', title='Amount')
            ]
        ).properties(width=700, height=400)
        st.altair_chart(summary_chart, use_container_width=True)

        with st.expander("View detailed transaction breakdown"):
            # Reuse the display formatting for the expandable detailed table.
            detailed_df = pd.DataFrame(transactions).rename(columns={
                "type": "Type",
                "category": "Category",
                "amount": "Amount (₹)",
                "date": "Date",
                "description": "Description",
            })
            detailed_df.index = range(1, len(detailed_df) + 1)
            detailed_df["Date"] = detailed_df["Date"].apply(format_date_value)
            detailed_df["Amount (₹)"] = detailed_df["Amount (₹)"].apply(format_rupees)
            st.dataframe(detailed_df)
    else:
        st.info("No transactions yet. Add some entries to generate your summary.")
