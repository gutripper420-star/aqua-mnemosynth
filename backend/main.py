import hmac
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from backend import database, hashing

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_FILENAME_LENGTH = 255
SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")


def create_app(db_path: str | Path = database.DB_PATH) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        database.init_db(db_path)
        yield

    app = FastAPI(title="Aqua Mnemosynth Evidence Integrity API", lifespan=lifespan)

    @app.post("/upload")
    async def upload_evidence(file: Annotated[UploadFile, File(...)]) -> dict[str, object]:
        filename = (file.filename or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
        if not filename or len(filename) > MAX_FILENAME_LENGTH:
            raise HTTPException(status_code=400, detail="Invalid filename.")

        contents = await file.read(MAX_UPLOAD_BYTES + 1)
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="File exceeds the 10 MiB upload limit.")

        file_hash = hashing.generate_sha256(contents)
        record_id = database.add_record(db_path, filename, file_hash)
        return {
            "status": "success",
            "record_id": record_id,
            "filename": filename,
            "sha256": file_hash,
        }

    @app.get("/verify/{filename}")
    async def verify_evidence(
        filename: str,
        provided_hash: Annotated[str, Query(min_length=64, max_length=64)],
    ) -> dict[str, str | bool]:
        if not SHA256_PATTERN.fullmatch(provided_hash):
            raise HTTPException(status_code=400, detail="provided_hash must be a SHA-256 digest.")

        record = database.get_record(db_path, filename)
        if record is None:
            raise HTTPException(status_code=404, detail="File not found in ledger.")

        stored_hash, timestamp = record
        normalized_hash = provided_hash.lower()
        return {
            "filename": filename,
            "match": hmac.compare_digest(stored_hash, normalized_hash),
            "stored_hash": stored_hash,
            "provided_hash": normalized_hash,
            "recorded_at": timestamp,
        }

    return app


app = create_app()
