import sqlite3

def revoke_key(key_id):

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE keys
        SET status='REVOKED'
        WHERE key_id=?
        """,
        (key_id,)
    )

    log_action(
    "REVOKE_KEY",
    f"Key ID {key_id}"
)

    conn.commit()
    conn.close()

    return True