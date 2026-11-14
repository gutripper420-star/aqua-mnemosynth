# Implementation Roadmap

This roadmap separates implemented repository features from proposed research
and future engineering. A roadmap entry is not evidence that a theory,
publication, deployment, or capability has been independently validated.

## Current status

The repository is a collection of documentation and two small software
prototypes. It is **not an operational AGLA-OSINT system and is not approved
for production or sensitive casework**.

| Area | Present state |
|---|---|
| Evidence prototype | FastAPI and Streamlit local prototype. Records a filename, SHA-256 digest, and timestamp in SQLite; it does not retain uploaded bytes or authenticate source identity. |
| Storage protections | SQLite triggers reject ordinary SQL updates and deletes. They do not prevent a person with database-file access from changing records or triggers. |
| Numerical model | `core/lattice.py` implements a real-hopping, one-dimensional Hatano–Nelson model with tests and a plotting command. It is not an OSINT, PHCA, or institutional-stability detector. |
| AGLA-OSINT | Described conceptually in project documentation; automated ingestion, entity resolution, graph analysis, falsification, and report generation are not implemented. |
| PHCA and Mnemosyne | Architectural concepts and documentation, not complete executable subsystems. |
| Deployment | Docker Compose supports local development. The API has no authentication and must not be exposed publicly or used for sensitive records. |

The status above is grounded in the code and documentation currently present.
The supplied claims about Project Prometheus, Phase II-F, the \(G_{E_2}\)
operator, \(\sigma_y\) feedback, the \(\lambda_{729}\) lattice, and associated
DOIs are **research statements to verify**, not implemented or independently
confirmed repository capabilities. Before citing the DOIs as evidence, verify
their metadata, availability, and contents against the source publications.
Do not describe the mathematics as proven by this repository.

## Proposed research record: Generation 11

The submitted “Non-Hermitian Control Engine” can be recorded as a proposed
research direction, subject to source verification. The supplied description
mentions PT-symmetric dimer modeling, an inversion gate, operator
classification, and a 729-point lattice. None of these are currently
implemented in this repository beyond the distinct Hatano–Nelson model noted
above.

Before any code is added, publish a precise mathematical specification:

- define the state space, operators, boundary conditions, parameters, and
  units;
- state assumptions and distinguish definitions, conjectures, and proved
  results;
- provide derivations and independently checkable references;
- define each prediction and its observation/falsification criteria;
- supply reproducible, non-sensitive example inputs and expected outputs;
- compare numerical results with analytic cases and document stability,
  precision, and failure modes.

The supplied DOI references may be added to a bibliography only after their
records and relevance have been checked. A DOI string or diagram alone does
not validate a result.

## Phases

### Phase 0 — Scope, claims, and research provenance

- [x] Document the proposed integrated architecture and its current-code limits.
- [ ] Establish a source bibliography for external papers, diagrams, and
  mathematical claims; record verification status and date.
- [ ] Define PHCA operationally, or keep it explicitly as an unimplemented
  conceptual term.
- [ ] Maintain a claim ledger separating source facts, mathematical results,
  hypotheses, and interpretations.
- [ ] Define acceptable uses and prohibited uses before collecting data.

**Exit condition:** every public technical claim is traceable to code, a
reproducible derivation, or a verified source, and its status is labeled.

### Phase 1 — Evidence and provenance model

- [ ] Define schemas for source references, claims, evidence, transformations,
  uncertainty, review decisions, and corrections.
- [ ] Record access basis, collection time, source locator, redactions, and
  known limitations.
- [ ] Define retention, deletion, export, backup, access, and correction
  policies before accepting real records.
- [ ] Keep source artifacts separate from normalized data and derived claims.
- [ ] Add tests for malformed inputs, duplicate records, corrections, and
  provenance preservation.

**Exit condition:** reviewers can trace every derived statement to its source
and transformation history without implying source authenticity from a hash.

### Phase 2 — Mathematical model verification

- [ ] Keep the existing Hatano–Nelson implementation and tests scoped to that
  model.
- [ ] For any proposed \(G_{E_2}\), \(\sigma_y\), PT-symmetric, or
  \(\lambda_{729}\) work, first add a separately reviewed mathematical
  specification and reproducible reference calculations.
- [ ] Test limiting cases, parameter boundaries, numerical precision, and
  independent implementations where practical.
- [ ] Record counterexamples and failed predictions alongside successful
  results.
- [ ] Do not connect mathematical outputs to claims about people or real
  institutions without validated measurement models and independent evidence.

**Exit condition:** each implemented equation has documented assumptions,
independent review, reproducible tests, and explicit limits on interpretation.

### Phase 3 — Bounded, system-level analysis

- [ ] Define analysis only for lawfully available, appropriately licensed,
  non-sensitive or properly governed data.
- [ ] Start with aggregate institutional indicators rather than person-level
  profiles or identity graphs.
- [ ] Specify baseline periods, denominators, missing-data behavior, confounders,
  and evaluation metrics before selecting thresholds.
- [ ] Treat threshold crossings as prompts for human review, never as findings
  of misconduct.
- [ ] Implement alternative-explanation and suppression records before any
  report-generation feature.

**Exit condition:** evaluation shows documented false-positive and
false-negative behavior on a representative, lawfully usable dataset, with
privacy and bias review completed.

### Phase 4 — Safety, security, and governance

- [ ] Establish a threat model, data classification, access controls, secure
  secret handling, and incident-response procedure.
- [ ] Add authentication and authorization before any non-local deployment.
- [ ] Replace or augment the prototype ledger with storage and audit controls
  appropriate to the stated integrity requirements; test backup and recovery.
- [ ] Define human review, independent challenge, correction, and appeal
  processes.
- [ ] Conduct privacy, security, bias, accessibility, and misuse reviews with
  qualified stakeholders.
- [ ] Prohibit suspect ranking, guilt-by-association outputs, covert collection,
  doxxing, and automated referrals or enforcement.

**Exit condition:** risks have owners and mitigations, independent review is
documented, and no unresolved critical issue affects the proposed deployment.

### Phase 5 — Limited pilot and release decision

- [ ] Use synthetic or otherwise approved data in an isolated test environment.
- [ ] Run scenario-based tests for ambiguity, conflicting records, false
  matches, missing data, privacy leaks, and correction requests.
- [ ] Publish a model card or equivalent describing intended use, evaluation,
  limits, and prohibited use.
- [ ] Obtain explicit approval from accountable technical, privacy, and domain
  reviewers for a narrowly defined pilot.
- [ ] Monitor errors and harms, provide a shutdown path, and review the pilot
  before expanding scope.

**Exit condition:** a named authority makes a documented release decision.
Passing tests or receiving multiple reviewer votes alone does not authorize
deployment.

## Operational readiness

The repository is **not ready for live operational use**. No deployment target,
data-access agreement, authentication model, privacy policy, independently
validated dataset, or approved operating authority is specified. Do not deploy
the current evidence prototype to a public network or load it with victim,
missing-person, child-welfare, medical, or other sensitive case data.

“Operational” must be defined for a specific environment and use. Readiness
requires completing the relevant phase gates above; it cannot be inferred from
a diagram, an article, a local Docker build, or a successful unit test.

## Definition of done for any feature

A feature is complete only when it has:

- a bounded purpose and documented specification;
- implementation and tests for expected and failure behavior;
- provenance and correction behavior where data or claims are involved;
- privacy, security, and misuse review proportional to impact;
- examples using synthetic or approved data;
- known limitations and a named human owner;
- documented review and release approval.
