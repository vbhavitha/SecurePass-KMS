import sqlite3

conn = sqlite3.connect(
    "database/kms.db"
)

cursor = conn.cursor()

search_value = input(
    "Enter Key ID or Key Name: "
)

# Check if input is numeric (ID)

if search_value.isdigit():

    cursor.execute(
        """
        SELECT *
        FROM keys
        WHERE key_id = ?
        """,
        (int(search_value),)
    )

else:

    cursor.execute(
        """
        SELECT *
        FROM keys
        WHERE key_name = ?
        """,
        (search_value,)
    )

result = cursor.fetchone()

if result:

    print("\n========== KEY DETAILS ==========\n")

    print("Key ID      :", result[0])
    print("Key Name    :", result[1])
    print("Key Type    :", result[2])
    print("Created At  :", result[3])
    print("Status      :", result[4])

    print("\n===============================")

else:

    print("\nNo key found.")

conn.close()