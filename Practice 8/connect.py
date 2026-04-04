import pg8000
from config import host, database, user, password, port


def connect():
    return pg8000.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=int(port)
    )