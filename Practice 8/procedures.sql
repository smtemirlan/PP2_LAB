CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE first_name = p_first_name AND last_name = p_last_name
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_first_name AND last_name = p_last_name;
    ELSE
        INSERT INTO phonebook(first_name, last_name, phone)
        VALUES (p_first_name, p_last_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(
    p_first_names VARCHAR[],
    p_last_names VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_first_names, 1) IS NULL
       OR array_length(p_last_names, 1) IS NULL
       OR array_length(p_phones, 1) IS NULL THEN
        RAISE EXCEPTION 'Arrays cannot be empty';
    END IF;

    IF array_length(p_first_names, 1) <> array_length(p_last_names, 1)
       OR array_length(p_first_names, 1) <> array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'All arrays must have the same length';
    END IF;

    CREATE TEMP TABLE IF NOT EXISTS invalid_data (
        first_name VARCHAR,
        last_name VARCHAR,
        phone VARCHAR,
        reason TEXT
    ) ON COMMIT PRESERVE ROWS;

    DELETE FROM invalid_data;

    FOR i IN 1..array_length(p_first_names, 1)
    LOOP
        IF p_phones[i] ~ '^87[0-9]{9}$' THEN
            IF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE first_name = p_first_names[i]
                  AND last_name = p_last_names[i]
            ) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE first_name = p_first_names[i]
                  AND last_name = p_last_names[i];
            ELSE
                INSERT INTO phonebook(first_name, last_name, phone)
                VALUES (p_first_names[i], p_last_names[i], p_phones[i]);
            END IF;
        ELSE
            INSERT INTO invalid_data(first_name, last_name, phone, reason)
            VALUES (
                p_first_names[i],
                p_last_names[i],
                p_phones[i],
                'Invalid phone format'
            );
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value
       OR last_name = p_value
       OR phone = p_value;
END;
$$;