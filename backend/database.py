import sqlite3


from .metadata import Config


def init_db():
    conn = sqlite3.connect(Config.DATABASE_URL)
    cursor = conn.cursor()
    cursor.executescript(Config.INIT_DB_SQL)
    conn.commit()
    cursor.close()
    conn.close()


def get_db():
    conn = sqlite3.connect(Config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
