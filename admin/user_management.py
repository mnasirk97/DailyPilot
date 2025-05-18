import streamlit as st
from core.database import load_users, save_users

def admin_panel():
    st.subheader("👤 Admin Panel - User Management")

    users = load_users()
    usernames = list(users.keys())

    # Show existing users
    st.write("### Existing Users:")
    for user in users:
        st.markdown(f"- **{user}** | Role: `{users[user]['role']}` | Apps: {users[user]['permissions']}")

    # Add new user
    st.write("### Create New User:")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ["user", "admin"])
    if st.button("Create User"):
        from core.auth import signup
        success = signup(new_user, new_pass, new_role)
        if success:
            st.success("User created!")
        else:
            st.error("User already exists.")

    # Assign permissions
    st.write("### Assign App Permissions:")
    target_user = st.selectbox("Select User", usernames)
    app_options = ["TimeGuardian", "NoteNest", "MoneyFlow", "HabitForge"]
    selected_apps = st.multiselect("Select Apps", app_options, default=users[target_user]["permissions"])
    if st.button("Update Permissions"):
        users[target_user]["permissions"] = selected_apps
        save_users(users)
        st.success("Permissions updated!")
