import sqlite3


def init_access_db():
    conn = sqlite3.connect("access.db")
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            role TEXT DEFAULT "user"
        )
    ''')

    # Таблица каналов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            channel_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
def add_user(user_id: int, role="user"):
    with sqlite3.connect("access.db") as conn:
        conn.execute("INSERT OR IGNORE INTO users (id, role) VALUES (?, ?)", (user_id, role))

def is_admin(user_id: int) -> bool:
    with sqlite3.connect("access.db") as conn:
        result = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()
        return result and result[0] == "admin"

def get_user_channels(user_id: int) -> list[str]:
    with sqlite3.connect("access.db") as conn:
        result = conn.execute("SELECT channel_id FROM channels WHERE user_id = ?", (user_id,)).fetchall()
        return [row[0] for row in result]

def add_channel(user_id: int, channel_id: str):
    with sqlite3.connect("access.db") as conn:
        conn.execute("INSERT INTO channels (user_id, channel_id) VALUES (?, ?)", (user_id, channel_id))

def remove_channel(user_id: int, channel_id: str):
    with sqlite3.connect("access.db") as conn:
        conn.execute("DELETE FROM channels WHERE user_id = ? AND channel_id = ?", (user_id, channel_id))
