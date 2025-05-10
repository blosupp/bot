import sqlite3

DB_PATH = "dialogues.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dialogue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def save_message(user_id: int, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO dialogue (user_id, role, content) VALUES (?, ?, ?)",
        (str(user_id), role, content)
    )
    conn.commit()
    conn.close()

def load_history(user_id: int, limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT role, content FROM dialogue WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (str(user_id), limit)
    )
    messages = [{"role": role, "content": content} for role, content in reversed(c.fetchall())]
    conn.close()
    return messages
