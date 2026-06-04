import sqlite3
from datetime import datetime

def log_action(action, details):

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs(
            action,
            details,
            created_at
        )
        VALUES (?, ?, ?)
        """,
        (
            action,
            details,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()