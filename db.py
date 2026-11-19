"""Data layer: tiny SQLite store for customer records.

Kept separate from the GUI so it can be tested on its own.
The database file lives next to the .exe (or next to this file when
running from source), so records survive between runs.
"""

import sqlite3
from pathlib import Path


def db_path() -> Path:
    # When frozen by PyInstaller, __file__ points inside the bundle,
    # so use the folder of the running executable instead.
    import sys

    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent / "records.db"
    return Path(__file__).parent / "records.db"


def init_db(path: Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(path or db_path())
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS records (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            phone   TEXT,
            notes   TEXT,
            created TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
        """
    )
    conn.commit()
    return conn


def add_record(conn, name: str, phone: str, notes: str) -> int:
    cur = conn.execute(
        "INSERT INTO records (name, phone, notes) VALUES (?, ?, ?)",
        (name.strip(), phone.strip(), notes.strip()),
    )
    conn.commit()
    return cur.lastrowid


def list_records(conn):
    cur = conn.execute(
        "SELECT id, name, phone, notes, created FROM records ORDER BY id DESC"
    )
    return cur.fetchall()


def delete_record(conn, record_id: int) -> None:
    conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
