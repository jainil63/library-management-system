import sqlite3
import os

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


def ensure_admin_user():
    conn = sqlite3.connect(Config.DATABASE_URL)
    conn.row_factory = sqlite3.Row  # Optional, for better dict-like row access
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        admin_exists = cursor.fetchone()

        if not admin_exists:
            cursor.execute(
                """
                INSERT INTO users (fullname, username, password, email, isadmin) 
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    Config.ADMIN_USER["fullname"],
                    Config.ADMIN_USER["username"],
                    Config.ADMIN_USER["password"],
                    Config.ADMIN_USER["email"],
                    1,
                ),
            )
            conn.commit()
            print("INFO:     Admin user created successfully!!!")
        else:
            print("INFO:     Admin user already exists!!!")

    except sqlite3.Error as e:
        raise Exception(f"ERROR:    An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()


def delete_db():
    os.remove(Config.DATABASE_URL)
