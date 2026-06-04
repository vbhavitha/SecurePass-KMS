import sqlite3

conn = sqlite3.connect(
    "database/kms.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS password_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    password_hash TEXT UNIQUE,

    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Password History Table Created")