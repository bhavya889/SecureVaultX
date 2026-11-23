import sqlite3
import time
from pathlib import Path


class VaultDatabase:
    """SQLite storage. Note content is encrypted before it reaches this class."""

    def __init__(self, data_dir):
        self.path = Path(data_dir) / "vaultx.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(str(self.path), timeout=15)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        with self._connect() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("""
                CREATE TABLE IF NOT EXISTS auth (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    master_salt BLOB NOT NULL,
                    wrapped_dek BLOB NOT NULL,
                    recovery_salt BLOB NOT NULL,
                    recovery_wrapped_dek BLOB NOT NULL
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    encrypted_data BLOB NOT NULL,
                    pinned INTEGER NOT NULL DEFAULT 0,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                )
            """)

    def save_auth(self, master_salt, wrapped_dek, recovery_salt, recovery_wrapped_dek):
        with self._connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO auth
                (id, master_salt, wrapped_dek, recovery_salt, recovery_wrapped_dek)
                VALUES (1, ?, ?, ?, ?)
            """, (master_salt, wrapped_dek, recovery_salt, recovery_wrapped_dek))

    def get_auth(self):
        with self._connect() as con:
            row = con.execute("SELECT * FROM auth WHERE id = 1").fetchone()
            return dict(row) if row else None

    def add_note(self, encrypted_data):
        now = time.time()
        with self._connect() as con:
            cursor = con.execute(
                "INSERT INTO notes (encrypted_data, created_at, updated_at) VALUES (?, ?, ?)",
                (encrypted_data, now, now),
            )
            return cursor.lastrowid

    def get_all_notes(self):
        with self._connect() as con:
            rows = con.execute(
                "SELECT id, encrypted_data, pinned FROM notes ORDER BY pinned DESC, updated_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]

    def delete_note(self, note_id):
        with self._connect() as con:
            con.execute("DELETE FROM notes WHERE id = ?", (note_id,))
