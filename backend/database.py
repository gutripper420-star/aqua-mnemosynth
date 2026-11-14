import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("EVIDENCE_DB_PATH", "data/evidence_ledger.db"))


def init_db(db_path: str | Path = DB_PATH) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TRIGGER IF NOT EXISTS prevent_update
            BEFORE UPDATE ON evidence
            BEGIN
                SELECT RAISE(ABORT, 'Updates are not allowed on the evidence ledger.');
            END
            """
        )
        conn.execute(
            """
            CREATE TRIGGER IF NOT EXISTS prevent_delete
            BEFORE DELETE ON evidence
            BEGIN
                SELECT RAISE(ABORT, 'Deletions are not allowed on the evidence ledger.');
            END
            """
        )


def add_record(db_path: str | Path, filename: str, sha256: str) -> int:
    timestamp = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO evidence (filename, sha256, timestamp) VALUES (?, ?, ?)",
            (filename, sha256, timestamp),
        )
        return int(cursor.lastrowid)


def get_record(db_path: str | Path, filename: str) -> tuple[str, str] | None:
    with sqlite3.connect(db_path) as conn:
        return conn.execute(
            "SELECT sha256, timestamp FROM evidence WHERE filename = ? "
            "ORDER BY id DESC LIMIT 1",
            (filename,),
        ).fetchone()
