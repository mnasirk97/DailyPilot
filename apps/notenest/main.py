import streamlit as st
import datetime
import os
import json

# File path per user
def get_notes_file(username):
    os.makedirs("data/notenest", exist_ok=True)
    return f"data/notenest/{username}_notes.json"

# Load notes
def load_notes(username):
    filepath = get_notes_file(username)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

# Save notes
def save_notes(username, notes):
    filepath = get_notes_file(username)
    with open(filepath, "w") as f:
        json.dump(notes, f, indent=4)

# Main app
def notenest_app(username):
    st.subheader("📝 NoteNest - Daily Notes")

    notes = load_notes(username)
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    st.write("### Write a New Note")
    new_note = st.text_area("Enter your note here...", height=150)

    if st.button("Save Note"):
        if date_str not in notes:
            notes[date_str] = []
        notes[date_str].append({
            "time": time_str,
            "note": new_note.strip()
        })
        save_notes(username, notes)
        st.success("Note saved!")

    st.write("### 🔍 View or Search Notes")
    search_date = st.date_input("Select Date to View Notes", datetime.date.today())
    search_str = st.text_input("Search by keyword (optional)")

    selected_date = search_date.strftime("%Y-%m-%d")
    if selected_date in notes:
        matched_notes = notes[selected_date]
        if search_str:
            matched_notes = [
                n for n in matched_notes if search_str.lower() in n["note"].lower()
            ]
        if matched_notes:
            for item in matched_notes:
                st.markdown(f"""
                - ⏰ `{item['time']}`  
                  📌 {item['note']}
                """)
        else:
            st.info("No matching notes found.")
    else:
        st.info("No notes for selected date.")
