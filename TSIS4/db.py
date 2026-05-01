import psycopg2

from config import load_config


def connect():
    # Подключается к базе
    try:
        config = load_config()
        return psycopg2.connect(**config)
    except Exception as error:
        print("Database error:", error)
        return None


def init_db():
    # Создает таблицы, если их нет
    conn = connect()

    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

        conn.commit()
        cur.close()

    except Exception as error:
        print("Init database error:", error)

    finally:
        conn.close()


def get_or_create_player(username):
    # Возвращает id игрока
    conn = connect()

    if conn is None:
        return None

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO players(username)
            VALUES (%s)
            ON CONFLICT (username) DO NOTHING;
        """, (username,))

        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        player_id = cur.fetchone()[0]

        conn.commit()
        cur.close()

        return player_id

    except Exception as error:
        print("Player error:", error)
        return None

    finally:
        conn.close()


def save_result(username, score, level):
    # Сохраняет результат игры
    player_id = get_or_create_player(username)

    if player_id is None:
        return

    conn = connect()

    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO game_sessions(player_id, score, level_reached)
            VALUES (%s, %s, %s);
        """, (player_id, score, level))

        conn.commit()
        cur.close()

    except Exception as error:
        print("Save result error:", error)

    finally:
        conn.close()


def get_top(limit=10):
    # Берет топ игроков из базы
    conn = connect()

    if conn is None:
        return []

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
            LIMIT %s;
        """, (limit,))

        rows = cur.fetchall()
        cur.close()

        return rows

    except Exception as error:
        print("Leaderboard error:", error)
        return []

    finally:
        conn.close()


def get_best_score(username):
    # Лучший счет конкретного игрока
    conn = connect()

    if conn is None:
        return 0

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COALESCE(MAX(gs.score), 0)
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            WHERE p.username = %s;
        """, (username,))

        best_score = cur.fetchone()[0]
        cur.close()

        return best_score

    except Exception as error:
        print("Best score error:", error)
        return 0

    finally:
        conn.close()
