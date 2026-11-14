import hashlib
import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend import database
from backend.main import MAX_REQUEST_BYTES, MAX_UPLOAD_BYTES, create_app

TEST_PASSWORD = "test-password-for-ledger"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("EVIDENCE_PASSWORD", TEST_PASSWORD)
    app = create_app(tmp_path / "data" / "ledger.db")
    with TestClient(app, auth=("mnemosyne", TEST_PASSWORD)) as test_client:
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


def test_upload_requires_correct_local_password(client):
    unauthorized = client.get("/health", auth=("mnemosyne", "wrong-password"))
    unauthorized_user = client.get(
        "/health", auth=("somebody-else", TEST_PASSWORD)
    )

    assert unauthorized.status_code == 401
    assert unauthorized_user.status_code == 401


def test_uploaded_file_can_be_verified_by_content(client):
    content = b"verify these bytes"
    recorded = client.post(
        "/upload",
        files={"file": ("original.txt", content, "text/plain")},
    )
    verified = client.post(
        "/verify",
        files={"file": ("renamed.txt", content, "text/plain")},
    )
    changed = client.post(
        "/verify",
        files={"file": ("original.txt", b"changed", "text/plain")},
    )

    assert recorded.status_code == 200
    assert verified.status_code == 200
    assert verified.json()["match"] is True
    assert verified.json()["recorded_filename"] == "original.txt"
    assert changed.status_code == 200
    assert changed.json()["match"] is False


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


def test_integrity_check_accepts_valid_ledger(client, tmp_path):
    client.post("/upload", files={"file": ("sample.txt", b"evidence")})

    database.check_integrity(tmp_path / "data" / "ledger.db")


def test_integrity_check_rejects_missing_append_only_trigger(client, tmp_path):
    db_path = tmp_path / "data" / "ledger.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TRIGGER prevent_update")

    with pytest.raises(sqlite3.DatabaseError, match="triggers are missing"):
        database.check_integrity(db_path)


def test_integrity_check_rejects_malformed_digest(client, tmp_path):
    db_path = tmp_path / "data" / "ledger.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TRIGGER prevent_update")
        conn.execute("UPDATE evidence SET sha256 = 'invalid'")
        conn.execute(
            """
            CREATE TRIGGER prevent_update
            BEFORE UPDATE ON evidence
            BEGIN
                SELECT RAISE(ABORT, 'Updates are not allowed on the evidence ledger.');
            END
            """
        )

    with pytest.raises(sqlite3.DatabaseError, match="invalid SHA-256"):
        database.check_integrity(db_path)
