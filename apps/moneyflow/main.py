import streamlit as st
import datetime
import os
import json

# File path
def get_money_file(username):
    os.makedirs("data/moneyflow", exist_ok=True)
    return f"data/moneyflow/{username}_money.json"

# Load money data
def load_money(username):
    filepath = get_money_file(username)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

# Save money data
def save_money(username, data):
    filepath = get_money_file(username)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# Main app
def moneyflow_app(username):
    st.subheader("💸 MoneyFlow - Track Income & Expenses")

    data = load_money(username)
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    st.write("### ➕ Add New Entry")
    entry_type = st.radio("Type", ["Expense", "Income"], horizontal=True)
    amount = st.number_input("Amount", min_value=0.0, step=10.0)
    category = st.text_input("Category (e.g. Food, Salary, Travel)")
    note = st.text_input("Note (optional)")

    if st.button("Save Entry"):
        new_entry = {
            "type": entry_type,
            "amount": amount,
            "category": category.strip(),
            "note": note.strip(),
            "time": current_time
        }

        if today not in data:
            data[today] = []
        data[today].append(new_entry)
        save_money(username, data)
        st.success(f"{entry_type} saved successfully!")

    # Filter by date
    st.write("### 📅 View Daily Summary")
    view_date = st.date_input("Select Date", datetime.date.today())
    selected_day = view_date.strftime("%Y-%m-%d")

    daily = data.get(selected_day, [])
    income_sum = sum(e["amount"] for e in daily if e["type"] == "Income")
    expense_sum = sum(e["amount"] for e in daily if e["type"] == "Expense")

    st.info(f"Total Income: ₹{income_sum:.2f} | Total Expense: ₹{expense_sum:.2f} | Balance: ₹{income_sum - expense_sum:.2f}")

    for e in daily:
        st.markdown(f"""
        - ⏰ `{e['time']}` | 💰 `{e['type']}` ₹{e['amount']}  
          📂 Category: {e['category']}  
          📝 {e['note'] or "_No note_"}
        """)

    # Monthly Summary
    st.write("### 📊 Monthly Overview")
    month = now.strftime("%Y-%m")
    monthly_income = 0
    monthly_expense = 0
    for d, entries in data.items():
        if d.startswith(month):
            for e in entries:
                if e["type"] == "Income":
                    monthly_income += e["amount"]
                else:
                    monthly_expense += e["amount"]

    st.success(f"Month-to-date: Income ₹{monthly_income:.2f} | Expense ₹{monthly_expense:.2f} | Savings ₹{monthly_income - monthly_expense:.2f}")
