# add_admin.py

import sqlite3

conn = sqlite3.connect("access.db")
cursor = conn.cursor()

# Вставь сюда свой Telegram ID
your_telegram_id = 1143201422

cursor.execute("INSERT OR IGNORE INTO users (id, role) VALUES (?, ?)", (your_telegram_id, "admin"))
conn.commit()
conn.close()

print("✅ Админ добавлен!")
