import sqlite3

DB_PATH = "access.db"

def init_access_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                role TEXT DEFAULT 'user',
                remember INTEGER DEFAULT 1,
                history_limit INTEGER DEFAULT 10,
                added_by INTEGER,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Таблица каналов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT,
                owner_id INTEGER,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
        """)

        conn.commit()


def add_user(user_id: int, role: str = "user", added_by: int = None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO users (id, role, added_by) VALUES (?, ?, ?)
        """, (user_id, role, added_by))
        conn.commit()


def remove_user(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()


def is_admin(user_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()
        return result and result[0] in ("admin", "superadmin")


def is_superadmin(user_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()
        return result and result[0] == "superadmin"


def get_user_settings(user_id: int) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT remember, history_limit, role FROM users WHERE id = ?
        """, (user_id,)).fetchone()
        if row:
            return {
                "remember": bool(row[0]),
                "history_limit": row[1],
                "role": row[2]
            }
        return {
            "remember": True,
            "history_limit": 10,
            "role": "user"
        }


def add_channel(user_id: int, channel_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO channels (channel_id, owner_id) VALUES (?, ?)
        """, (channel_id, user_id))
        conn.commit()


def remove_channel(user_id: int, channel_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            DELETE FROM channels WHERE owner_id = ? AND channel_id = ?
        """, (user_id, channel_id))
        conn.commit()


def get_user_channels(user_id: int) -> list[str]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT channel_id FROM channels WHERE owner_id = ?
        """, (user_id,)).fetchall()
        return [r[0] for r in rows]
