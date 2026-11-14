"""Mnemosyne Local: password-protected SHA-256 evidence ledger (local prototype).

Only filename, digest and timestamp are stored; uploaded bytes are hashed in memory.
"""
import hashlib
import hmac
import os
import re
import sqlite3
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(title="Mnemosyne Local")
security = HTTPBasic()
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def db_path() -> str:
    return os.environ.get("EVIDENCE_DB_PATH", "evidence.db")


def get_password() -> str:
    pw = os.environ.get("EVIDENCE_PASSWORD", "")
    if len(pw) < 12 or not all(32 <= ord(c) < 127 for c in pw):
        raise HTTPException(503, "EVIDENCE_PASSWORD must be set (12+ printable ASCII characters)")
    return pw


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.execute(
        "CREATE TABLE IF NOT EXISTS evidence ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, "
        "sha256 TEXT NOT NULL, created_at TEXT NOT NULL)"
    )
    conn.execute(
        "CREATE TRIGGER IF NOT EXISTS evidence_no_update BEFORE UPDATE ON evidence "
        "BEGIN SELECT RAISE(ABORT, 'ledger is append-only'); END"
    )
    conn.execute(
        "CREATE TRIGGER IF NOT EXISTS evidence_no_delete BEFORE DELETE ON evidence "
        "BEGIN SELECT RAISE(ABORT, 'ledger is append-only'); END"
    )
    return conn


def auth(creds: HTTPBasicCredentials = Depends(security)) -> None:
    expected = get_password().encode()
    if not hmac.compare_digest(creds.password.encode(), expected):
        raise HTTPException(401, "Invalid password", headers={"WWW-Authenticate": "Basic"})


async def digest(file: UploadFile) -> str:
    h = hashlib.sha256()
    while chunk := await file.read(1024 * 1024):
        h.update(chunk)
    return h.hexdigest()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/evidence", dependencies=[Depends(auth)])
async def add_evidence(file: UploadFile = File(...)):
    name = os.path.basename(file.filename or "")
    if not name:
        raise HTTPException(400, "Filename required")
    sha = await digest(file)
    ts = datetime.now(timezone.utc).isoformat()
    conn = connect()
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO evidence (filename, sha256, created_at) VALUES (?, ?, ?)",
                (name, sha, ts),
            )
        return {"id": cur.lastrowid, "filename": name, "sha256": sha, "created_at": ts}
    finally:
        conn.close()


@app.get("/evidence", dependencies=[Depends(auth)])
def list_evidence():
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT id, filename, sha256, created_at FROM evidence ORDER BY id DESC"
        ).fetchall()
    finally:
        conn.close()
    return [dict(zip(("id", "filename", "sha256", "created_at"), r)) for r in rows]


def latest(filename: str):
    conn = connect()
    try:
        return conn.execute(
            "SELECT sha256, created_at FROM evidence WHERE filename = ? ORDER BY id DESC LIMIT 1",
            (filename,),
        ).fetchone()
    finally:
        conn.close()


@app.post("/verify", dependencies=[Depends(auth)])
async def verify_file(file: UploadFile = File(...)):
    name = os.path.basename(file.filename or "")
    row = latest(name)
    if row is None:
        raise HTTPException(404, "No record for filename")
    sha = await digest(file)
    return {"filename": name, "match": hmac.compare_digest(sha, row[0]),
            "sha256": sha, "recorded_sha256": row[0], "recorded_at": row[1]}


@app.get("/verify/{filename}/{sha256}", dependencies=[Depends(auth)])
def verify_hash(filename: str, sha256: str):
    if not HEX64.match(sha256):
        raise HTTPException(422, "sha256 must be 64 hexadecimal characters")
    row = latest(filename)
    if row is None:
        raise HTTPException(404, "No record for filename")
    return {"filename": filename, "match": hmac.compare_digest(sha256.lower(), row[0]),
            "recorded_at": row[1]}
