import sqlite3

conn = sqlite3.connect(
    "database/kms.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs(

    log_id INTEGER PRIMARY KEY AUTOINCREMENT,

    action TEXT,

    details TEXT,

    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Audit Table Created")