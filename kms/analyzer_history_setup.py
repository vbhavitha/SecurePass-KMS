import sqlite3

conn = sqlite3.connect(
    "database/kms.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS analyzer_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    strength TEXT,

    entropy REAL,

    breach TEXT,

    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Analyzer History Created")