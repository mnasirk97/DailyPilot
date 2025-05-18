import streamlit as st
from apps.timeguardian.main import timeguardian_app
from apps.notenest.main import notenest_app
from apps.moneyflow.main import moneyflow_app
from apps.habitpulse.main import habitpulse_app
from apps.admin.main import admin_dashboard

import json
import os

# Load users data
def load_users():
    filepath = "data/users.json"
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

# Login system
def login():
    st.title("🔐 DailyPilot Login")

    users = load_users()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in users and users[username]["password"] == password:
            st.success(f"Welcome, {username}!")
            st.session_state.username = username
        else:
            st.error("Invalid credentials.")

# Main routing
def main():
    if "username" not in st.session_state:
        login()
        return

    username = st.session_state.username
    users = load_users()

    if username == "admin":
        available_apps = {
            "TimeGuardian": True,
            "NoteNest": True,
            "MoneyFlow": True,
            "HabitPulse": True
        }
    else:
        available_apps = users.get(username, {}).get("apps", {})

    st.sidebar.title("📱 Select App")
    app_list = ["Admin Dashboard"] if username == "admin" else []

    if available_apps.get("TimeGuardian"):
        app_list.append("TimeGuardian")
    if available_apps.get("NoteNest"):
        app_list.append("NoteNest")
    if available_apps.get("MoneyFlow"):
        app_list.append("MoneyFlow")
    if available_apps.get("HabitPulse"):
        app_list.append("HabitPulse")

    app_choice = st.sidebar.selectbox("Apps", app_list)

    st.sidebar.write("👤 Logged in as:", username)
    if st.sidebar.button("Logout"):
        del st.session_state.username
        st.experimental_rerun()

    if app_choice == "Admin Dashboard":
        admin_dashboard(username)
    elif app_choice == "TimeGuardian":
        timeguardian_app(username)
    elif app_choice == "NoteNest":
        notenest_app(username)
    elif app_choice == "MoneyFlow":
        moneyflow_app(username)
    elif app_choice == "HabitPulse":
        habitpulse_app(username)

if __name__ == "__main__":
    main()



# import streamlit as st
# from apps.admin.main import admin_dashboard
# from apps.timeguardian.main import timeguardian_app
# from apps.notenest.main import notenest_app
# from apps.moneyflow.main import moneyflow_app
# from core.auth import login
# from admin.user_management import admin_panel

# st.set_page_config(page_title="DailyPilot", layout="centered")

# st.title("🚀 DailyPilot - Personal Productivity System")

# # --- Login Form ---
# st.sidebar.header("Login")
# username = st.sidebar.text_input("Username")
# password = st.sidebar.text_input("Password", type="password")

# if st.sidebar.button("Login"):
#     user = login(username, password)
#     if user:
#         st.session_state["user"] = user
#         st.session_state["username"] = username
#         st.success(f"Welcome, {username}!")
#     else:
#         st.error("Invalid credentials")

# # --- Logged in area ---
# # if "user" in st.session_state:
# #     user = st.session_state["user"]
# #     username = st.session_state["username"]
# #     st.sidebar.success(f"Logged in as {username}")

# #     if user["role"] == "admin":
# #         admin_panel()
# #     else:
# #         st.info("App access coming soon based on permissions...")




# # Logged in
# if "user" in st.session_state:
#     user = st.session_state["user"]
#     username = st.session_state["username"]
#     st.sidebar.success(f"Logged in as {username}")

#     if user["role"] == "admin":
#         admin_panel()
#     else:
#         app_choice = st.sidebar.selectbox("📂 Select App", user["permissions"])

#         # if app_choice == "TimeGuardian":
#         #     timeguardian_app(username)
#         # if app_choice == "TimeGuardian":
#         #     timeguardian_app(username)
#         # elif app_choice == "NoteNest":
#         #     notenest_app(username)
#         # else:
#         #     st.warning("That app is not implemented yet.")
#         if app_choice == "TimeGuardian":
#             timeguardian_app(username)
#         elif app_choice == "NoteNest":
#             notenest_app(username)
#         elif app_choice == "MoneyFlow":
#             moneyflow_app(username)
#         else:
#             st.warning("That app is not implemented yet.")

