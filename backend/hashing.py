import hashlib


def generate_sha256(file_bytes: bytes) -> str:
    """Return the SHA-256 digest of the provided bytes."""
    return hashlib.sha256(file_bytes).hexdigest()
