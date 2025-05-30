import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        level INTEGER DEFAULT 1,
        clicks INTEGER DEFAULT 0,
        nova INTEGER DEFAULT 0,
        referrals INTEGER DEFAULT 0,
        last_active DATE DEFAULT CURRENT_DATE
    )
    """)
    conn.commit()
    conn.close()

def get_user_data(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
    conn.close()
    return dict(zip(["user_id", "username", "level", "clicks", "nova", "referrals", "last_active"], row))

def increment_clicks(user_id, amount=1):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET clicks = clicks + ?, last_active = date('now') WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()
