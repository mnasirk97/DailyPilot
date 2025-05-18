import streamlit as st
import datetime
import os
import json

# File path
def get_habits_file(username):
    os.makedirs("data/habitpulse", exist_ok=True)
    return f"data/habitpulse/{username}_habits.json"

# Load habit data
def load_habits(username):
    filepath = get_habits_file(username)
    if not os.path.exists(filepath):
        return {"habits": [], "log": {}}
    with open(filepath, "r") as f:
        return json.load(f)

# Save habit data
def save_habits(username, data):
    filepath = get_habits_file(username)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# Main App
def habitpulse_app(username):
    st.subheader("🔁 HabitPulse - Track Your Daily Habits")

    data = load_habits(username)
    habits = data["habits"]
    log = data["log"]
    today = datetime.date.today().isoformat()

    # Add new habit
    st.write("### ➕ Add New Habit")
    new_habit = st.text_input("Enter a new habit (e.g. Drink Water, Walk 30 mins)")
    if st.button("Add Habit"):
        if new_habit.strip() and new_habit not in habits:
            habits.append(new_habit.strip())
            save_habits(username, {"habits": habits, "log": log})
            st.success("Habit added successfully!")

    if not habits:
        st.warning("No habits added yet.")
        return

    # Daily habit checkboxes
    st.write("### ✅ Mark Today's Habits")
    completed_today = log.get(today, [])

    for habit in habits:
        checked = habit in completed_today
        if st.checkbox(habit, value=checked, key=habit):
            if habit not in completed_today:
                completed_today.append(habit)
        else:
            if habit in completed_today:
                completed_today.remove(habit)

    log[today] = completed_today
    save_habits(username, {"habits": habits, "log": log})

    # Daily summary
    st.write("### 📅 Today's Progress")
    total = len(habits)
    done = len(completed_today)
    st.info(f"Completed: {done}/{total} habits")

    # Weekly summary
    st.write("### 📈 Weekly Overview")
    last_7_days = [(datetime.date.today() - datetime.timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

    for day in last_7_days:
        habits_done = log.get(day, [])
        st.markdown(f"**{day}**: {len(habits_done)}/{total} habits")

    # Overall summary
    st.write("### 📊 Habit Completion Stats")
    habit_counts = {habit: 0 for habit in habits}
    total_days = len(log)

    for entries in log.values():
        for h in entries:
            habit_counts[h] += 1

    for h, count in habit_counts.items():
        st.markdown(f"- `{h}`: completed on **{count}/{total_days}** days")
