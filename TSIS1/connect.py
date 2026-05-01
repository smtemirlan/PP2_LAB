import psycopg2
from config import load_config

def connect():
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None
