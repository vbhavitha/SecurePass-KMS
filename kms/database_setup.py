import sqlite3

conn = sqlite3.connect(
    "database/kms.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS keys (

    key_id INTEGER PRIMARY KEY AUTOINCREMENT,

    key_name TEXT,

    key_type TEXT,

    created_at TEXT,

    status TEXT
)
""")

conn.commit()

conn.close()

print("KMS Database Created Successfully")