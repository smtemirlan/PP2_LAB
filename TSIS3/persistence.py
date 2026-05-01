import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
SETTINGS_FILE = BASE_DIR / "settings.json"
LEADERBOARD_FILE = BASE_DIR / "leaderboard.json"


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_settings():
    # Загружает настройки
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(data)
        return settings

    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    # Сохраняет настройки
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    # Загружает таблицу лидеров
    if not LEADERBOARD_FILE.exists():
        save_leaderboard([])
        return []

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def save_leaderboard(scores):
    # Сохраняет таблицу лидеров
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def add_score(name, score, distance, coins):
    # Добавляет новый результат
    scores = load_leaderboard()

    scores.append({
        "name": name,
        "score": score,
        "distance": distance,
        "coins": coins
    })

    scores.sort(key=lambda item: item["score"], reverse=True)
    scores = scores[:10]

    save_leaderboard(scores)
