# aqua-mnemosynth
Aqua Mnemosynth: a mythotechnical system for symbolic computation, PHCA analysis, recursive inference, and liability-risk modeling.

## Evidence integrity prototype

The repository includes a local evidence-recording prototype. It stores uploaded
file names, SHA-256 digests, and timestamps in SQLite, and provides a Streamlit
interface and FastAPI endpoint for comparing a supplied digest with the latest
record for a filename.

Run both services with Docker Compose:

```bash
docker compose up --build
```

Open the interface at <http://localhost:8501> and the API documentation at
<http://localhost:8000/docs>. The backend also runs directly with
`uvicorn backend.main:app --reload`; install backend dependencies first.

Uploads are limited to 10 MiB. SQLite triggers prevent updates and deletions
through ordinary SQL operations, but this is not immutable or independently
audited storage: anyone with database-file access can alter the database or
remove its triggers. The prototype does not authenticate users, validate source
identity, or provide a substitute for forensic chain-of-custody controls.
