import streamlit as st
import datetime
import os
import json

# File path for saving time data
def get_time_file(username):
    os.makedirs("data/timeguardian", exist_ok=True)
    return f"data/timeguardian/{username}_time.json"

# Load saved data
def load_time_data(username):
    filepath = get_time_file(username)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

# Save data
def save_time_data(username, data):
    filepath = get_time_file(username)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# Main app function
def timeguardian_app(username):
    st.subheader("🕒 TimeGuardian - Track Your Office Hours")

    data = load_time_data(username)
    today = str(datetime.date.today())

    st.write("### Set Your Office Hours (Default: 9:00 AM - 5:00 PM)")
    office_start = st.time_input("Office Start Time", datetime.time(9, 0))
    office_end = st.time_input("Office End Time", datetime.time(17, 0))

    st.write("### Log Today’s In/Out Time")
    in_time = st.time_input("In Time", datetime.datetime.now().time())
    out_time = st.time_input("Out Time", datetime.datetime.now().time())

    if st.button("Save Today’s Log"):
        total_minutes = (
            datetime.datetime.combine(datetime.date.today(), out_time) -
            datetime.datetime.combine(datetime.date.today(), in_time)
        ).seconds // 60
        office_minutes = (
            datetime.datetime.combine(datetime.date.today(), office_end) -
            datetime.datetime.combine(datetime.date.today(), office_start)
        ).seconds // 60

        status = []
        if in_time > office_start:
            status.append("Late In")
        if out_time < office_end:
            status.append("Early Out")

        data[today] = {
            "in": in_time.strftime("%H:%M"),
            "out": out_time.strftime("%H:%M"),
            "total_time": f"{total_minutes // 60}h {total_minutes % 60}m",
            "status": " | ".join(status) if status else "On Time"
        }

        save_time_data(username, data)
        st.success("Log saved for today!")

    st.write("### 📅 Previous Logs")
    for date, log in sorted(data.items(), reverse=True):
        st.markdown(f"""
        - **{date}**  
          ⏰ In: `{log['in']}` | Out: `{log['out']}`  
          🧮 Time Spent: `{log['total_time']}`  
          🔍 Status: `{log['status']}`
        """)
