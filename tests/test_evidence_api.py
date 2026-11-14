import hashlib
import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend.main import MAX_REQUEST_BYTES, MAX_UPLOAD_BYTES, create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(tmp_path / "data" / "ledger.db")
    with TestClient(app) as test_client:
        yield test_client


def test_upload_and_verify_latest_hash(client):
    content = b"evidence"
    uploaded = client.post(
        "/upload",
        files={"file": ("sample.txt", content, "text/plain")},
    )

    assert uploaded.status_code == 200
    record = uploaded.json()
    assert record["sha256"] == hashlib.sha256(content).hexdigest()

    verified = client.get(
        "/verify/sample.txt",
        params={"provided_hash": record["sha256"].upper()},
    )
    assert verified.status_code == 200
    assert verified.json()["match"] is True


def test_mismatched_hash_and_missing_record(client):
    client.post("/upload", files={"file": ("sample.txt", b"evidence")})

    mismatch = client.get(
        "/verify/sample.txt",
        params={"provided_hash": hashlib.sha256(b"other").hexdigest()},
    )
    missing = client.get(
        "/verify/missing.txt",
        params={"provided_hash": hashlib.sha256(b"other").hexdigest()},
    )

    assert mismatch.status_code == 200
    assert mismatch.json()["match"] is False
    assert missing.status_code == 404


def test_rejects_oversized_upload(client):
    response = client.post(
        "/upload",
        files={"file": ("large.bin", b"x" * (MAX_UPLOAD_BYTES + 1))},
    )

    assert response.status_code == 413


def test_rejects_oversized_request_body_before_parsing(client):
    response = client.post(
        "/upload",
        files={"file": ("large.bin", b"x" * MAX_REQUEST_BYTES)},
    )

    assert response.status_code == 413


def test_ledger_triggers_reject_updates_and_deletes(client, tmp_path):
    db_path = tmp_path / "data" / "ledger.db"
    client.post("/upload", files={"file": ("sample.txt", b"evidence")})

    with sqlite3.connect(db_path) as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE evidence SET filename = 'changed.txt'")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("DELETE FROM evidence")
