# aqua-mnemosynth
Aqua Mnemosynth: a mythotechnical system for symbolic computation, PHCA analysis, recursive inference, and liability-risk modeling.

## Integrated architecture

The [integrated architecture](Integrated-Architecture.md) combines the
Digital Organism lineage and AGLA-OSINT methodology while distinguishing
conceptual claims from implemented features and unverified case-study
assertions.

The [implementation roadmap](Roadmap.md) tracks current status, research
verification, and safety gates. The repository is not currently ready for
public operational deployment.

See the [Aqua Mnemosyne overview](Aqua-Mnemosyne-Overview.md) for a
15-section encyclopedia-style summary, an original illustration, and a
description of proposed safeguards and current implementation limits.

## Mnemosyne Local MVP

The local MVP hashes uploaded files in memory and stores only their filenames,
SHA-256 digests, and timestamps in SQLite. It does not parse or retain file
contents. It verifies a later upload by comparing its digest with recorded
digests; a match demonstrates byte equality with a recorded digest, not source
identity, authorship, or truth.

Set a local password (at least 12 characters) and run both services:

```bash
export EVIDENCE_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(24))')"
docker compose up --build
```

Open the interface at <http://127.0.0.1:8501>. The API is also available on
<http://127.0.0.1:8000> for local development. Both published ports bind to
loopback, and the API requires HTTP Basic authentication using the local
password. For direct backend development, set `EVIDENCE_PASSWORD` and
`EVIDENCE_DB_PATH`, then run `uvicorn backend.main:app --reload`.

Uploads are limited to 10 MiB. The ledger rejects ordinary SQL updates and
deletes, and startup checks SQLite structure, digest formatting, timestamps,
and append-only triggers. These checks do not detect a privileged user
rewriting a valid digest or replacing the database. The password gates the API;
it does not encrypt the SQLite file at rest. Protect the local machine and
backups, use only non-sensitive documents, and do not expose this service to a
network. The GitHub Actions workflow runs tests against temporary synthetic
ledgers; it never receives or checks a user's private local ledger.

The cryptographic hash-chain and user-provided-dataset anomaly analysis remain
future phases. No OSINT scraping, profiling, facial recognition, or connection
to police or intelligence databases is implemented.

## Hatano–Nelson lattice foundation

The `core/lattice.py` module provides the real-hopping Hatano–Nelson matrix,
generalized Brillouin zone radius and continuum, open-boundary spectrum, and
eigenstate center-of-mass calculations. Install `requirements-science.txt` to
run the lattice tests or generate the skin-effect and GBZ plot:

```bash
python -m pip install -r requirements-science.txt
python -m scripts.plot_skinfx --output skinfx.png
```

The model uses upper/lower hopping entries `t + gamma` and `t - gamma`;
the periodic-boundary option is available through `hatano_nelson`.
