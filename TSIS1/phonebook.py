import csv
import json
from connect import connect

VALID_TYPES = {"home", "work", "mobile"}
DEFAULT_GROUPS = {"family": "Family", "work": "Work", "friend": "Friend", "other": "Other"}


def fix_empty(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def fix_group(value):
    value = fix_empty(value)
    if not value:
        return "Other"
    return DEFAULT_GROUPS.get(value.lower(), value)


def fix_phone_type(value):
    value = fix_empty(value)
    if not value:
        return "mobile"
    value = value.lower()
    if value not in VALID_TYPES:
        return "mobile"
    return value


def ensure_group(cur, group_name):
    group_name = fix_group(group_name)

    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def save_contact(cur, username, email, birthday, group_name):
    group_id = ensure_group(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts(username, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO UPDATE SET
            email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (username, fix_empty(email), fix_empty(birthday), group_id)
    )

    return cur.fetchone()[0]


def save_phone(cur, contact_id, phone, phone_type):
    phone = fix_empty(phone)
    if not phone:
        return

    cur.execute(
        """
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (phone) DO NOTHING
        """,
        (contact_id, phone, fix_phone_type(phone_type))
    )


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        username, email, birthday, group_name, phones = row
        print("-" * 60)
        print("Name:     ", username)
        print("Email:    ", email or "-")
        print("Birthday: ", birthday or "-")
        print("Group:    ", group_name or "-")
        print("Phones:   ", phones or "-")


def add_contact():
    username = input("Username: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email (optional): ").strip()
    birthday = input("Birthday YYYY-MM-DD (optional): ").strip()
    group_name = input("Group (Family/Work/Friend/Other): ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        contact_id = save_contact(cur, username, email, birthday, group_name)
        save_phone(cur, contact_id, phone, phone_type)
        conn.commit()
        print("Contact saved.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()


def show_all_contacts(order_by="c.id"):
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            f"""
            SELECT
                c.username,
                c.email,
                c.birthday,
                g.name,
                COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '') AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON p.contact_id = c.id
            GROUP BY c.id, c.username, c.email, c.birthday, g.name
            ORDER BY {order_by}
            """
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def search_by_function():
    query = input("Search text: ").strip()

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()

        if not rows:
            print("No results.")
            return

        for username, email, birthday, group_name, phone, phone_type in rows:
            print("-" * 60)
            print("Name:     ", username)
            print("Email:    ", email or "-")
            print("Birthday: ", birthday or "-")
            print("Group:    ", group_name or "-")
            print("Phone:    ", phone or "-", phone_type or "")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def filter_by_group():
    group_name = input("Group name: ").strip()

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                c.username,
                c.email,
                c.birthday,
                g.name,
                COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '') AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON p.contact_id = c.id
            WHERE g.name ILIKE %s
            GROUP BY c.id, c.username, c.email, c.birthday, g.name
            ORDER BY c.username
            """,
            (group_name,)
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def search_by_email():
    email_part = input("Email contains: ").strip()

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                c.username,
                c.email,
                c.birthday,
                g.name,
                COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '') AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON p.contact_id = c.id
            WHERE c.email ILIKE %s
            GROUP BY c.id, c.username, c.email, c.birthday, g.name
            ORDER BY c.username
            """,
            (f"%{email_part}%",)
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def sorted_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by created date")
    choice = input("Choice: ").strip()

    if choice == "1":
        show_all_contacts("c.username")
    elif choice == "2":
        show_all_contacts("c.birthday NULLS LAST")
    elif choice == "3":
        show_all_contacts("c.created_at")
    else:
        print("Wrong choice.")


def pagination():
    page = 0
    limit = 3

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        while True:
            offset = page * limit

            cur.execute(
                """
                SELECT
                    c.username,
                    c.email,
                    c.birthday,
                    g.name,
                    COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '') AS phones
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON p.contact_id = c.id
                GROUP BY c.id, c.username, c.email, c.birthday, g.name
                ORDER BY c.id
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )

            rows = cur.fetchall()

            if not rows and page > 0:
                page -= 1
                print("No next page.")
                continue

            print("\nPage:", page + 1)
            print_contacts(rows)

            command = input("\nnext / prev / quit: ").strip().lower()

            if command == "next":
                page += 1
            elif command == "prev":
                if page > 0:
                    page -= 1
            elif command == "quit":
                break
            else:
                print("Unknown command.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def add_phone_to_contact():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip()

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, fix_phone_type(phone_type)))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()


def move_contact_to_group():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("CALL move_to_group(%s, %s)", (name, fix_group(group_name)))
        conn.commit()
        print("Contact moved.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()


def import_csv():
    filename = input("CSV filename: ").strip() or "contacts.csv"

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                username = fix_empty(row.get("username"))
                if not username:
                    continue

                contact_id = save_contact(
                    cur,
                    username,
                    row.get("email"),
                    row.get("birthday"),
                    row.get("group")
                )

                save_phone(
                    cur,
                    contact_id,
                    row.get("phone"),
                    row.get("phone_type")
                )

        conn.commit()
        print("CSV imported.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()


def export_json():
    filename = input("JSON filename: ").strip() or "contactsExport.json"

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT c.id, c.username, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            """
        )

        contacts = []

        for contact_id, username, email, birthday, group_name in cur.fetchall():
            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
                (contact_id,)
            )

            phones = []
            for phone, phone_type in cur.fetchall():
                phones.append({
                    "phone": phone,
                    "type": phone_type
                })

            contacts.append({
                "username": username,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group_name,
                "phones": phones
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)

        print("JSON exported to", filename)
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def import_json():
    filename = input("JSON filename: ").strip() or "sampleData.json"

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            username = fix_empty(item.get("username"))
            if not username:
                continue

            cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
            exists = cur.fetchone()

            if exists:
                answer = input(f"{username} already exists. skip/overwrite? ").strip().lower()
                if answer == "skip":
                    continue

            contact_id = save_contact(
                cur,
                username,
                item.get("email"),
                item.get("birthday"),
                item.get("group")
            )

            for phone_item in item.get("phones", []):
                save_phone(
                    cur,
                    contact_id,
                    phone_item.get("phone"),
                    phone_item.get("type")
                )

        conn.commit()
        print("JSON imported.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()


def menu():
    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Search by name/email/phone")
        print("4. Filter by group")
        print("5. Search by email")
        print("6. Sort contacts")
        print("7. Pagination")
        print("8. Add phone to existing contact")
        print("9. Move contact to group")
        print("10. Import CSV")
        print("11. Export JSON")
        print("12. Import JSON")
        print("0. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_all_contacts()
        elif choice == "3":
            search_by_function()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            search_by_email()
        elif choice == "6":
            sorted_contacts()
        elif choice == "7":
            pagination()
        elif choice == "8":
            add_phone_to_contact()
        elif choice == "9":
            move_contact_to_group()
        elif choice == "10":
            import_csv()
        elif choice == "11":
            export_json()
        elif choice == "12":
            import_json()
        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Wrong choice.")


if __name__ == "__main__":
    menu()
