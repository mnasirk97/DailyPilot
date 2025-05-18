import streamlit as st
import os
import json

USERS_FILE = "data/users.json"

# Load users
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users
def save_users(data):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Admin Panel
def admin_dashboard(username):
    if username != "admin":
        st.error("Access Denied. Admins only.")
        return

    st.subheader("🛠 Admin Dashboard - Manage Users & App Access")
    users = load_users()

    # Add new user
    st.write("### ➕ Add New User")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Create User"):
        if new_user in users:
            st.warning("User already exists.")
        else:
            users[new_user] = {
                "password": new_pass,
                "apps": {
                    "TimeGuardian": False,
                    "NoteNest": False,
                    "MoneyFlow": False,
                    "HabitPulse": False
                }
            }
            save_users(users)
            st.success(f"User `{new_user}` created!")

    st.divider()

    # View & edit users
    st.write("### 👥 Existing Users")
    for user, info in users.items():
        if user == "admin":
            continue
        st.markdown(f"**👤 {user}**")

        cols = st.columns(5)
        for i, app in enumerate(["TimeGuardian", "NoteNest", "MoneyFlow", "HabitPulse"]):
            enabled = info["apps"].get(app, False)
            new_val = cols[i].checkbox(f"{app}", value=enabled, key=f"{user}_{app}")
            info["apps"][app] = new_val

        if cols[4].button("🗑 Delete", key=f"del_{user}"):
            del users[user]
            save_users(users)
            st.warning(f"User `{user}` deleted.")
            st.experimental_rerun()

    save_users(users)
