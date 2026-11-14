# Intellectual Property and Publications Index

This is an author-supplied index of frameworks, publications and links. Entries are the author's own claims and descriptions. **None has been independently reviewed or verified by this repository**, and none is implemented here unless the "Status" column says so. Third-party audit subjects are listed by title only; this index makes no factual assertions about them.

## Frameworks and protocols

| Name | Author's description | Status in this repository |
| --- | --- | --- |
| Project Prometheus | Linear drift model A(s) = A₀ + s·A₁ with parametric bootstrap for Bogdanov-Takens bifurcation detection | Not implemented; unverified pending source and math review |
| Non-Smooth Byzantine Fault Tolerance (NS-BFT) | 729-node lattice consensus (N = 729, F = 242, Q = 485) | Quorum arithmetic only: `backend/quorum.py`. Finding: Q = 485 is safe for N = 727, but N = 729 needs Q = 486 |
| MedSecure | SHA-256 hash-chained, zero-plaintext data layer for patient data | Hash chain implemented in `backend/main.py` for evidence files; no HIPAA claim is made |
| The Kindness Gate | Ethical constraint hierarchy: Sovereign Consent, Non-Hierarchical Application, Auditability | Conceptual; not implemented |
| PHCA-016 V2 Operator | Baseline damping plus cascade hierarchy aimed at global asymptotic stability | Not implemented; stability claim unverified |
| Negative Exchange Equation (NEE) | Penalty algorithm for slashing security bonds of malicious nodes | Not implemented; unverified |
| Ed25519 signatures | Consensus signature standard | Not implemented |
| EpCross storage | Flat-file append-only binary format (Flatbuffers) | Not implemented; the current ledger is SQLite |
| JSON-LD genesis payload | `genesis-v1.7.0-beta.jsonld` binding of the V2 Operator and Λ729 lattice | Not in this repository |

The Mnemosyne "quantum search-and-destroy / dead man's switch" concept and the biological-sovereignty framework (PDC-BIO-2026-01) are deliberately **not** implemented or specified here. They are speculative, unreviewed, and outside the scope of an evidence-integrity tool.

## Publications and links (as supplied)

- Academia.edu: https://independentresearcher.academia.edu/AnthonyBlair
- Zenodo record: https://zenodo.org/records/23258325
- Live engine: https://epcross-uenlwshz.manus.space/
- Code: https://github.com/anthonyjblair8-source/Sentinel-Cardio-The-global-integrity-audit
- Further Zenodo and prior-art documents were supplied as `share.google` links (Founding Charter of Systems Pathology, Mathematical Framework and Prior Art, PHCA Simulator v1.6.0, The Unified Framework, Digital Twin Specifications, Prior Art and Legal Research, Sovereign Convergence). Shortened links should be replaced with permanent DOIs before being cited.

## Usage notes

- Citation counts, visibility rankings and "prior art" status are claims to be backed by dated, public records (for example, Zenodo DOIs). A hash recorded in this ledger proves a file existed in that form at a recorded time, not who authored it or that it is novel.
- See `Roadmap.md` and `Architecture.md` for how these items relate to the planned work.
