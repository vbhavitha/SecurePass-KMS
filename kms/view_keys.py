import sqlite3

conn = sqlite3.connect(
    "database/kms.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT *
    FROM keys
    """
)

rows = cursor.fetchall()

print("\nKEY INVENTORY\n")

print(
    "ID\tKEY NAME\tTYPE\tSTATUS\tCREATED AT"
)

print("-" * 80)

for row in rows:

    print(
        f"{row[0]}\t{row[1]}\t{row[2]}\t{row[4]}\t{row[3]}"
    )

conn.close()