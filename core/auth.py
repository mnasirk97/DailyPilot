import hashlib
from core.database import load_users, save_users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    users = load_users()
    hashed = hash_password(password)
    if username in users and users[username]["password"] == hashed:
        return users[username]
    return None

def signup(username, password, role="user"):
    users = load_users()
    if username in users:
        return False  # User already exists
    users[username] = {
        "password": hash_password(password),
        "role": role,
        "permissions": []
    }
    save_users(users)
    return True
