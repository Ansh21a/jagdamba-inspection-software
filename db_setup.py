from __future__ import annotations

import sqlite3
from pathlib import Path

APP_DB_NAME = "inspection_software.db"


def db_path() -> Path:
    # DB lives next to app.py in the project root
    return Path(__file__).resolve().parent / APP_DB_NAME


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path()))
    return conn


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "username TEXT UNIQUE, "
        "password TEXT, "
        "role TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS party_master("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "party_name TEXT, "
        "address TEXT, "
        "gst_no TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS inspector_master("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "inspector_name TEXT, "
        "designation TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS reports("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "party TEXT, "
        "inspector TEXT, "
        "insp_date TEXT)"
    )

    cur.execute(
        "INSERT OR IGNORE INTO users(username,password,role) "
        "VALUES('admin','admin123','admin')"
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized/verified at: {db_path()}")

