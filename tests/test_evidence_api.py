import hashlib

import pytest
from fastapi.testclient import TestClient

from backend.main import app

PW = "correct-horse-battery"
AUTH = ("user", PW)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("EVIDENCE_DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setenv("EVIDENCE_PASSWORD", PW)
    return TestClient(app)


def test_requires_auth(client):
    assert client.get("/evidence").status_code == 401
    assert client.get("/evidence", auth=("u", "wrong-password-x")).status_code == 401


def test_unset_password_rejected(client, monkeypatch):
    monkeypatch.setenv("EVIDENCE_PASSWORD", "short")
    assert client.get("/evidence", auth=AUTH).status_code == 503


def test_record_and_verify(client):
    data = b"evidence"
    r = client.post("/evidence", files={"file": ("a.txt", data)}, auth=AUTH)
    sha = hashlib.sha256(data).hexdigest()
    assert r.json()["sha256"] == sha
    ok = client.post("/verify", files={"file": ("a.txt", data)}, auth=AUTH).json()
    assert ok["match"] is True
    bad = client.post("/verify", files={"file": ("a.txt", b"tampered")}, auth=AUTH).json()
    assert bad["match"] is False
    assert client.get(f"/verify/a.txt/{sha}", auth=AUTH).json()["match"] is True
    assert client.get("/verify/a.txt/zz", auth=AUTH).status_code == 422
    assert client.post("/verify", files={"file": ("none", b"x")}, auth=AUTH).status_code == 404


def test_latest_record_wins_and_history_kept(client):
    client.post("/evidence", files={"file": ("a.txt", b"one")}, auth=AUTH)
    client.post("/evidence", files={"file": ("a.txt", b"two")}, auth=AUTH)
    assert len(client.get("/evidence", auth=AUTH).json()) == 2
    assert client.post("/verify", files={"file": ("a.txt", b"two")}, auth=AUTH).json()["match"]
