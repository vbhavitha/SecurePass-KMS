import sqlite3
from datetime import datetime


def save_analysis(
    strength,
    entropy,
    breach
):

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analyzer_history(
            strength,
            entropy,
            breach,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            strength,
            entropy,
            breach,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()