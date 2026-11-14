import hashlib
import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend.main import app

PW = "correct-horse-battery"
AUTH = ("admin", PW)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("EVIDENCE_DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setenv("EVIDENCE_PASSWORD", PW)
    return TestClient(app)


def add_user(client, name, role, pw="another-long-password"):
    r = client.post("/users", json={"username": name, "password": pw, "role": role}, auth=AUTH)
    assert r.status_code == 201
    return (name, pw)


def test_requires_auth(client):
    assert client.get("/evidence").status_code == 401
    assert client.get("/evidence", auth=("admin", "wrong-password-x")).status_code == 401
    assert client.get("/evidence", auth=("nobody", PW)).status_code == 401


def test_unset_password_rejected(client, monkeypatch):
    monkeypatch.setenv("EVIDENCE_PASSWORD", "short")
    assert client.get("/evidence", auth=AUTH).status_code == 503


def test_record_and_verify(client):
    data = b"evidence"
    r = client.post("/evidence", files={"file": ("a.txt", data)}, data={"case_id": "c1"}, auth=AUTH)
    sha = hashlib.sha256(data).hexdigest()
    assert r.json()["sha256"] == sha
    ok = client.post("/verify", files={"file": ("a.txt", data)}, data={"case_id": "c1"}, auth=AUTH).json()
    assert ok["match"] is True
    bad = client.post("/verify", files={"file": ("a.txt", b"x")}, data={"case_id": "c1"}, auth=AUTH).json()
    assert bad["match"] is False
    assert client.get(f"/verify/c1/a.txt/{sha}", auth=AUTH).json()["match"] is True
    assert client.get("/verify/c1/a.txt/zz", auth=AUTH).status_code == 422
    # same filename in another case has no record
    assert client.post("/verify", files={"file": ("a.txt", data)}, data={"case_id": "c2"}, auth=AUTH).status_code == 404


def test_latest_record_wins_and_history_kept(client):
    client.post("/evidence", files={"file": ("a.txt", b"one")}, auth=AUTH)
    client.post("/evidence", files={"file": ("a.txt", b"two")}, auth=AUTH)
    assert len(client.get("/evidence", auth=AUTH).json()) == 2
    assert client.post("/verify", files={"file": ("a.txt", b"two")}, auth=AUTH).json()["match"]


def test_roles(client):
    analyst, auditor = add_user(client, "ann", "analyst"), add_user(client, "aud", "auditor")
    assert client.post("/evidence", files={"file": ("a", b"1")}, auth=analyst).json()["actor"] == "ann"
    assert client.post("/evidence", files={"file": ("a", b"1")}, auth=auditor).status_code == 403
    assert client.get("/ledger/verify-chain", auth=analyst).status_code == 403
    assert client.get("/ledger/verify-chain", auth=auditor).json()["valid"] is True
    body = {"username": "mallory", "password": PW, "role": "analyst"}
    assert client.post("/users", json=body, auth=analyst).status_code == 403
    assert client.post("/users", json={**body, "username": "ann"}, auth=AUTH).status_code == 409
    assert client.post("/users", json={**body, "role": "admin"}, auth=AUTH).status_code == 422


def test_chain_detects_tampering(client, tmp_path):
    for i in range(3):
        client.post("/evidence", files={"file": (f"f{i}", b"d%d" % i)}, auth=AUTH)
    res = client.get("/ledger/verify-chain", auth=AUTH).json()
    assert res["valid"] and res["entries"] == 3 and len(res["head"]) == 64

    # a privileged attacker drops the triggers and rewrites a hash
    conn = sqlite3.connect(tmp_path / "t.db")
    conn.execute("DROP TRIGGER ledger_no_update")
    conn.execute("UPDATE ledger SET sha256 = ? WHERE id = 2", ("0" * 64,))
    conn.commit()
    conn.close()
    res = client.get("/ledger/verify-chain", auth=AUTH).json()
    assert res == {"valid": False, "entries": 3, "first_bad_id": 2, "head": None}
    assert client.get("/ledger/export", auth=AUTH).json()["chain"]["valid"] is False


def test_triggers_block_ordinary_edits(client, tmp_path):
    client.post("/evidence", files={"file": ("a", b"1")}, auth=AUTH)
    conn = sqlite3.connect(tmp_path / "t.db")
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("DELETE FROM ledger")
