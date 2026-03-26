import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table is ready.")


def insert_from_console():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added successfully.")


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row["name"], row["phone"])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported from CSV successfully.")


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id;")
    rows = cur.fetchall()

    if rows:
        print("\nContacts:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def search_contacts():
    print("\nSearch by:")
    print("1. Name")
    print("2. Phone prefix")
    choice = input("Choose an option: ").strip()

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name or part of name: ").strip()
        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s",
            (f"%{name}%",)
        )
    elif choice == "2":
        prefix = input("Enter phone prefix: ").strip()
        cur.execute(
            "SELECT * FROM contacts WHERE phone LIKE %s",
            (f"{prefix}%",)
        )
    else:
        print("Invalid option.")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()

    if rows:
        print("\nSearch results:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No matching contacts found.")

    cur.close()
    conn.close()


def update_contact():
    print("\nUpdate by:")
    print("1. Name")
    print("2. Phone")
    choice = input("Choose an option: ").strip()

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        old_name = input("Enter current name: ").strip()
        new_name = input("Enter new name: ").strip()
        cur.execute(
            "UPDATE contacts SET name = %s WHERE name = %s",
            (new_name, old_name)
        )
    elif choice == "2":
        name = input("Enter contact name: ").strip()
        new_phone = input("Enter new phone: ").strip()
        cur.execute(
            "UPDATE contacts SET phone = %s WHERE name = %s",
            (new_phone, name)
        )
    else:
        print("Invalid option.")
        cur.close()
        conn.close()
        return

    conn.commit()

    if cur.rowcount > 0:
        print("Contact updated successfully.")
    else:
        print("No contact found.")

    cur.close()
    conn.close()


def delete_contact():
    print("\nDelete by:")
    print("1. Name")
    print("2. Phone")
    choice = input("Choose an option: ").strip()

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name to delete: ").strip()
        cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
    elif choice == "2":
        phone = input("Enter phone to delete: ").strip()
        cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
    else:
        print("Invalid option.")
        cur.close()
        conn.close()
        return

    conn.commit()

    if cur.rowcount > 0:
        print("Contact deleted successfully.")
    else:
        print("No contact found.")

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Create table")
        print("2. Add contact from console")
        print("3. Import contacts from CSV")
        print("4. Show all contacts")
        print("5. Search contacts")
        print("6. Update contact")
        print("7. Delete contact")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv("contacts.csv")
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            update_contact()
        elif choice == "7":
            delete_contact()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


menu()