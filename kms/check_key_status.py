import sqlite3

key_name = input("Enter Key Name: ")

conn = sqlite3.connect(
    "database/kms.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT status
    FROM keys
    WHERE key_name=?
    """,
    (key_name,)
)

result = cursor.fetchone()

conn.close()

if result:

    status = result[0]

    print("Status:", status)

    if status == "REVOKED":

        raise Exception(
            "Key has been revoked"
        )

    print("Key can be used")

else:

    print("Key not found")