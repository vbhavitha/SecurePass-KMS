import sqlite3
import hashlib
from datetime import datetime


def password_exists(password):

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM password_history
        WHERE password_hash=?
        """,
        (password_hash,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_password(password):

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO password_history(
            password_hash,
            created_at
        )
        VALUES (?, ?)
        """,
        (
            password_hash,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()