from configparser import ConfigParser
from pathlib import Path

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()

    # Ищем database.ini в той же папке, где лежит config.py
    file_path = Path(__file__).parent / filename
    parser.read(file_path)

    config = {}
    if parser.has_section(section):
        for key, value in parser.items(section):
            config[key] = value
    else:
        raise Exception(f"Section {section} not found in {file_path}")

    return config

if __name__ == '__main__':
    print(load_config())
