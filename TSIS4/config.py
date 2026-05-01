from configparser import ConfigParser
from pathlib import Path


def load_config(filename="database.ini", section="postgresql"):
    # Читает настройки PostgreSQL из database.ini
    path = Path(__file__).parent / filename

    parser = ConfigParser()
    parser.read(path)

    if not parser.has_section(section):
        raise Exception(f"Section {section} not found in {path}")

    config = {}
    for key, value in parser.items(section):
        config[key] = value

    return config
