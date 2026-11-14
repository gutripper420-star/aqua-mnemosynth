import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("EVIDENCE_DB_PATH", "data/evidence_ledger.db"))
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def init_db(db_path: str | Path = DB_PATH) -> None:
    path = Path(db_path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
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
    if os.name == "posix":
        path.chmod(0o600)


def check_integrity(db_path: str | Path = DB_PATH) -> None:
    """Raise DatabaseError when SQLite or ledger records fail basic checks."""
    with sqlite3.connect(db_path) as conn:
        result = conn.execute("PRAGMA integrity_check").fetchone()
        if result is None or result[0] != "ok":
            raise sqlite3.DatabaseError("SQLite integrity check failed.")

        triggers = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'trigger' "
                "AND tbl_name = 'evidence'"
            )
        }
        if not {"prevent_update", "prevent_delete"}.issubset(triggers):
            raise sqlite3.DatabaseError("Append-only ledger triggers are missing.")

        for sha256, timestamp in conn.execute(
            "SELECT sha256, timestamp FROM evidence"
        ):
            if not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
                raise sqlite3.DatabaseError("Ledger contains an invalid SHA-256 digest.")
            try:
                datetime.fromisoformat(timestamp)
            except (TypeError, ValueError) as exc:
                raise sqlite3.DatabaseError("Ledger contains an invalid timestamp.") from exc


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


def get_record_by_hash(
    db_path: str | Path, sha256: str
) -> tuple[int, str, str] | None:
    with sqlite3.connect(db_path) as conn:
        return conn.execute(
            "SELECT id, filename, timestamp FROM evidence WHERE sha256 = ? "
            "ORDER BY id DESC LIMIT 1",
            (sha256,),
        ).fetchone()
