"""Mnemosyne: multi-user, hash-chained SHA-256 evidence ledger.

Only filename, digest, case ID, actor and timestamp are stored; uploaded bytes are
hashed in memory. Every entry commits to the previous entry's hash, so any edit,
deletion or reordering of history is detectable via /ledger/verify-chain.
"""
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI(title="Mnemosyne", version="0.2.0")
security = HTTPBasic()
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
USERNAME = re.compile(r"^[A-Za-z0-9_.-]{3,64}$")
GENESIS = "0" * 64
ADMIN = "admin"
ROLES = {
    "admin": {"record", "read", "audit", "manage"},
    "analyst": {"record", "read"},
    "auditor": {"read", "audit"},
}
PBKDF2_ROUNDS = 200_000


def db_path() -> str:
    return os.environ.get("EVIDENCE_DB_PATH", "evidence.db")


def valid_password(pw: str) -> bool:
    return len(pw) >= 12 and all(32 <= ord(c) < 127 for c in pw)


def admin_password() -> str:
    pw = os.environ.get("EVIDENCE_PASSWORD", "")
    if not valid_password(pw):
        raise HTTPException(503, "EVIDENCE_PASSWORD must be set (12+ printable ASCII characters)")
    return pw


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path(), isolation_level=None)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS ledger ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL, filename TEXT NOT NULL, "
        "sha256 TEXT NOT NULL, actor TEXT NOT NULL, created_at TEXT NOT NULL, "
        "prev_hash TEXT NOT NULL, entry_hash TEXT NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "username TEXT PRIMARY KEY, role TEXT NOT NULL, salt TEXT NOT NULL, pw_hash TEXT NOT NULL)"
    )
    for op in ("UPDATE", "DELETE"):
        conn.execute(
            f"CREATE TRIGGER IF NOT EXISTS ledger_no_{op.lower()} BEFORE {op} ON ledger "
            "BEGIN SELECT RAISE(ABORT, 'ledger is append-only'); END"
        )
    return conn


def entry_hash(prev: str, case_id: str, filename: str, sha: str, actor: str, ts: str) -> str:
    payload = "\x1f".join((prev, case_id, filename, sha, actor, ts)).encode()
    return hashlib.sha256(payload).hexdigest()


def hash_pw(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ROUNDS).hex()


class User:
    def __init__(self, username: str, role: str):
        self.username, self.role = username, role


def authenticate(creds: HTTPBasicCredentials = Depends(security)) -> User:
    fail = HTTPException(401, "Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    if creds.username == ADMIN:
        if hmac.compare_digest(creds.password.encode(), admin_password().encode()):
            return User(ADMIN, "admin")
        raise fail
    conn = connect()
    try:
        row = conn.execute(
            "SELECT role, salt, pw_hash FROM users WHERE username = ?", (creds.username,)
        ).fetchone()
    finally:
        conn.close()
    salt = bytes.fromhex(row[1]) if row else b"\0" * 16
    candidate = hash_pw(creds.password, salt)
    if row is None or not hmac.compare_digest(candidate, row[2]):
        raise fail
    return User(creds.username, row[0])


def require(permission: str):
    def dep(user: User = Depends(authenticate)) -> User:
        if permission not in ROLES[user.role]:
            raise HTTPException(403, f"Role '{user.role}' lacks '{permission}' permission")
        return user
    return dep


async def digest(file: UploadFile) -> str:
    h = hashlib.sha256()
    while chunk := await file.read(1024 * 1024):
        h.update(chunk)
    return h.hexdigest()


def clean_name(file: UploadFile) -> str:
    name = os.path.basename(file.filename or "")
    if not name:
        raise HTTPException(400, "Filename required")
    return name


def clean_case(case_id: str) -> str:
    case_id = case_id.strip()
    if not case_id or len(case_id) > 128:
        raise HTTPException(400, "case_id must be 1-128 characters")
    return case_id


COLS = "id, case_id, filename, sha256, actor, created_at, prev_hash, entry_hash"


def row_dict(r) -> dict:
    return dict(zip(COLS.split(", "), r))


@app.get("/health")
def health():
    return {"status": "ok"}


class NewUser(BaseModel):
    username: str
    password: str
    role: str


@app.post("/users", status_code=201)
def create_user(body: NewUser, _: User = Depends(require("manage"))):
    if not USERNAME.match(body.username) or body.username == ADMIN:
        raise HTTPException(422, "Invalid username")
    if body.role not in ROLES or body.role == "admin":
        raise HTTPException(422, "role must be 'analyst' or 'auditor'")
    if not valid_password(body.password):
        raise HTTPException(422, "password must be 12+ printable ASCII characters")
    salt = secrets.token_bytes(16)
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (body.username, body.role, salt.hex(), hash_pw(body.password, salt)),
        )
    except sqlite3.IntegrityError:
        raise HTTPException(409, "User exists")
    finally:
        conn.close()
    return {"username": body.username, "role": body.role}


@app.post("/evidence")
async def add_evidence(
    file: UploadFile = File(...),
    case_id: str = Form("default"),
    user: User = Depends(require("record")),
):
    name, case_id = clean_name(file), clean_case(case_id)
    sha = await digest(file)
    ts = datetime.now(timezone.utc).isoformat()
    conn = connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        last = conn.execute("SELECT entry_hash FROM ledger ORDER BY id DESC LIMIT 1").fetchone()
        prev = last[0] if last else GENESIS
        eh = entry_hash(prev, case_id, name, sha, user.username, ts)
        cur = conn.execute(
            "INSERT INTO ledger (case_id, filename, sha256, actor, created_at, prev_hash, entry_hash) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (case_id, name, sha, user.username, ts, prev, eh),
        )
        conn.execute("COMMIT")
        return {"id": cur.lastrowid, "case_id": case_id, "filename": name, "sha256": sha,
                "actor": user.username, "created_at": ts, "entry_hash": eh}
    finally:
        conn.close()


@app.get("/evidence")
def list_evidence(case_id: str | None = None, _: User = Depends(require("read"))):
    conn = connect()
    try:
        if case_id:
            rows = conn.execute(
                f"SELECT {COLS} FROM ledger WHERE case_id = ? ORDER BY id DESC", (case_id,)
            ).fetchall()
        else:
            rows = conn.execute(f"SELECT {COLS} FROM ledger ORDER BY id DESC").fetchall()
    finally:
        conn.close()
    return [row_dict(r) for r in rows]


def latest(filename: str, case_id: str):
    conn = connect()
    try:
        return conn.execute(
            "SELECT sha256, created_at FROM ledger WHERE filename = ? AND case_id = ? "
            "ORDER BY id DESC LIMIT 1",
            (filename, case_id),
        ).fetchone()
    finally:
        conn.close()


@app.post("/verify")
async def verify_file(
    file: UploadFile = File(...),
    case_id: str = Form("default"),
    _: User = Depends(require("read")),
):
    name, case_id = clean_name(file), clean_case(case_id)
    row = latest(name, case_id)
    if row is None:
        raise HTTPException(404, "No record for filename in this case")
    sha = await digest(file)
    return {"filename": name, "case_id": case_id, "match": hmac.compare_digest(sha, row[0]),
            "sha256": sha, "recorded_sha256": row[0], "recorded_at": row[1]}


@app.get("/verify/{case_id}/{filename}/{sha256}")
def verify_hash(case_id: str, filename: str, sha256: str, _: User = Depends(require("read"))):
    if not HEX64.match(sha256):
        raise HTTPException(422, "sha256 must be 64 hexadecimal characters")
    row = latest(filename, case_id)
    if row is None:
        raise HTTPException(404, "No record for filename in this case")
    return {"filename": filename, "case_id": case_id,
            "match": hmac.compare_digest(sha256.lower(), row[0]), "recorded_at": row[1]}


def all_rows():
    conn = connect()
    try:
        return conn.execute(f"SELECT {COLS} FROM ledger ORDER BY id ASC").fetchall()
    finally:
        conn.close()


def check_chain(rows) -> dict:
    prev = GENESIS
    for r in rows:
        e = row_dict(r)
        expected = entry_hash(prev, e["case_id"], e["filename"], e["sha256"], e["actor"], e["created_at"])
        if e["prev_hash"] != prev or not hmac.compare_digest(e["entry_hash"], expected):
            return {"valid": False, "entries": len(rows), "first_bad_id": e["id"], "head": None}
        prev = e["entry_hash"]
    return {"valid": True, "entries": len(rows), "first_bad_id": None, "head": prev}


@app.get("/ledger/verify-chain")
def verify_chain(_: User = Depends(require("audit"))):
    return check_chain(all_rows())


@app.get("/ledger/export")
def export_ledger(case_id: str | None = None, _: User = Depends(require("audit"))):
    """Chain verification result plus entries; the head hash can be anchored externally."""
    rows = all_rows()
    entries = [row_dict(r) for r in rows if not case_id or r[1] == case_id]
    return {"exported_at": datetime.now(timezone.utc).isoformat(),
            "chain": check_chain(rows), "entries": entries}
