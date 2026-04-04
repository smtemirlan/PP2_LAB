from pathlib import Path
from connect import connect

BASE_DIR = Path(__file__).resolve().parent


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def load_sql_file(filename):
    filepath = BASE_DIR / filename

    with open(filepath, "r", encoding="utf-8") as file:
        sql = file.read()

    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def insert_or_update(first_name, last_name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_or_update_user(%s, %s, %s);",
        (first_name, last_name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def search_by_pattern(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_phonebook(%s);", (pattern,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def get_paginated(limit_value, offset_value):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_phonebook_paginated(%s, %s);",
        (limit_value, offset_value)
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def insert_many(first_names, last_names, phones):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many_users(%s, %s, %s);",
        (first_names, last_names, phones)
    )

    cur.execute("SELECT * FROM invalid_data;")
    invalid_rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return invalid_rows


def delete_by_value(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s);", (value,))

    conn.commit()
    cur.close()
    conn.close()


def print_rows(rows):
    if not rows:
        print("No data found.")
        return

    for row in rows:
        print(row)


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert or update user")
        print("2. Search by pattern")
        print("3. Show paginated results")
        print("4. Insert many users")
        print("5. Delete user")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            phone = input("Enter phone: ")

            insert_or_update(first_name, last_name, phone)
            print("User inserted or updated successfully.")

        elif choice == "2":
            pattern = input("Enter search pattern: ")
            rows = search_by_pattern(pattern)
            print_rows(rows)

        elif choice == "3":
            limit_value = int(input("Enter limit: "))
            offset_value = int(input("Enter offset: "))
            rows = get_paginated(limit_value, offset_value)
            print_rows(rows)

        elif choice == "4":
            n = int(input("How many users do you want to add? "))

            first_names = []
            last_names = []
            phones = []

            for i in range(n):
                print(f"\nUser {i + 1}:")
                first_names.append(input("Enter first name: "))
                last_names.append(input("Enter last name: "))
                phones.append(input("Enter phone: "))

            invalid_rows = insert_many(first_names, last_names, phones)

            print("\nUsers processed.")
            if invalid_rows:
                print("Invalid data:")
                print_rows(invalid_rows)
            else:
                print("All users inserted successfully.")

        elif choice == "5":
            value = input("Enter first name, last name, or phone to delete: ")
            delete_by_value(value)
            print("Matching user(s) deleted successfully.")

        elif choice == "6":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    try:
        create_table()
        load_sql_file("functions.sql")
        load_sql_file("procedures.sql")
        menu()
    except Exception as e:
        print("ERROR:", e)