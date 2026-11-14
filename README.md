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

## Hatano–Nelson lattice foundation

The `core/lattice.py` module provides the real-hopping Hatano–Nelson matrix,
generalized Brillouin zone radius and continuum, open-boundary spectrum, and
eigenstate center-of-mass calculations. Install `requirements-science.txt` to
run the lattice tests or generate the skin-effect and GBZ plot:

```bash
python -m pip install -r requirements-science.txt
python scripts/plot_skinfx.py --output skinfx.png
```

The model uses upper/lower hopping entries `t + gamma` and `t - gamma`;
the periodic-boundary option is available through `hatano_nelson`.
