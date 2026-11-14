# Integrated Digital Organism and AGLA-OSINT Architecture

## Status and scope

This document combines the supplied *Digital Organism* evolutionary record with
the AGLA-OSINT operator's field guide into one conceptual architecture for Aqua
Mnemosynth. It describes a proposed, human-reviewed system for evidence
management and institutional process analysis. It is not a claim that the
named frameworks, historical artifacts, case-study findings, or deployments
have been independently verified.

The supplied EFTA/DOJ case-study assertions—including amounts, interpretations,
and allegations about named people or organizations—are intentionally not
reproduced as findings. They require independent verification against cited
primary sources and appropriate legal, privacy, and editorial review before
publication. The material itself also identifies source code, schemas, query
sets, and raw outputs as pending, so its operational-readiness and successful
validation claims are not established by the material provided.

## Purpose and governing idea

The system is intended to help reviewers represent records, examine
system-level patterns, test explanations, and document uncertainty. The
“Digital Organism” is treated as a metaphor for an evolving collection of
methods and components, not an autonomous agent. The central constraint is:

> Observe and preserve evidence; analyze mechanisms; test alternatives; protect
> affected people; leave consequential decisions to accountable human reviewers.

It is a decision-support concept, not an enforcement, surveillance, or
investigative targeting system. It must not issue accusations, identify
individuals as wrongdoers, or initiate coercive action.

## Evolutionary lineage

The supplied ten-generation narrative can be read as a conceptual progression.
These entries describe the submitted framework history, not independently
verified releases or implementations.

| Generation | Theme | Contribution to the integrated design |
|---|---|---|
| 0 | Origin concept | Constraint-based protocols for detecting institutional drift |
| 1 | Aletheia-Core | Replace retaliation or intervention with passive diagnostics |
| 2 | The Lost Study | Add cultural and historical context |
| 3 | Quantum integrity | Emphasize transmission integrity and metadata protection |
| 4 | Mnemosyne | Preserve provenance, context, and revision history |
| 5 | STASIS anomaly | Explore persistent deviations as a diagnostic model |
| 6 | AGLA | Establish the Observe–Project–Pattern–Break–Rotate review cycle |
| 7 | Biomechanization | Extend the proposed scope to biology; this architecture does not implement or endorse human genetic modification |
| 8 | AGLA-OSINT | Organize public-record analysis around normalization, correlation, falsification, and ethics |
| 9 | Compendiums | Apply the conceptual method across historical and cultural domains |
| 10 | Unified organism | Bring evidence, formal analysis, interpretation, ethics, and review into one model |

The progression is useful as a design narrative, not as evidence that any
capability is validated or operational.

## Integrated architecture

### Three evidence and interpretation layers

1. **Empirical layer:** Source artifacts, document identifiers, dates, page
   references, and records of how material was acquired. Preserve source
   limitations and access restrictions.
2. **Formal layer:** Normalization, entity and event references, relationship
   hypotheses, comparison methods, thresholds, alternatives, and falsification
   results. Every transformation should be reproducible.
3. **Interpretive layer:** Context, ethical assessment, limitations, and
   system-level recommendations. Interpretations must not be used to validate
   empirical claims.

### Functional components

| Component | Role | Required constraint |
|---|---|---|
| PHCA / constraint analysis | Describe context, phases, boundaries, and candidate deviations | Define variables and assumptions; do not treat a model score as proof |
| Mnemosyne / provenance | Track source metadata, transformations, and revisions | Retain corrections and uncertainty; do not promise immutability without independent controls |
| RCP / recursive review | Compare hypotheses and update confidence as evidence changes | Show why confidence changed; permit unresolved and competing explanations |
| Shadow Multiplicatio / Blade | Try to falsify correlations and identify alternative explanations | A failed check suppresses the claim, not the underlying source record |
| Flamewalker | Keep empirical, formal, and interpretive content distinct | No interpretive conclusion may upgrade an unsupported source claim |
| AGLA cycle | Coordinate analyst review | Every cycle records observations, decisions, suppressions, and recalibration |
| Kindness Gate | Review potential harms before sharing outputs | Minimize personal data; protect victims and vulnerable people; quarantine unsafe outputs |
| Council / distributed review | Provide independent review perspectives | Agreement among tools or reviewers is not proof; disclose conflicts and preserve dissent |

### Evidence workflow

```text
Authorized public sources
  -> source and access record
  -> normalization with provenance
  -> candidate entity/event links
  -> system-level comparison
  -> alternative explanations and falsification
  -> privacy and harm review
  -> human-reviewed, qualified report
  -> corrections and versioned audit trail
```

Ingestion should be limited to sources that are lawfully and openly accessible
for the stated purpose. The workflow must not bypass access controls, obtain
private account data, or infer sensitive facts about private individuals.
Sensitive victim, missing-person, child-welfare, and medical information should
not be collected into general-purpose analysis datasets. Where specially
authorized access is required, it needs a separate governed process and
qualified review.

## AGLA operator cycle

| Step | Activity | Record in the review |
|---|---|---|
| **Observe** | Capture a source artifact or measure a system-level indicator | Source, date, exact locator, collection method, limitations |
| **Project** | State a bounded question and intended use | Decision owner, scope, affected groups, exclusions |
| **Pattern** | Compare records or aggregate system indicators | Method, baseline, candidate relationship, uncertainty |
| **Break** | Attempt to disconfirm the candidate explanation | Alternative explanations, failure conditions, source checks |
| **Rotate** | Revise the model and preserve the review history | What changed, why, remaining gaps, next review |

Moving from Break to Rotate is mandatory. A failed falsification check suppresses
the proposed inference; it does not authorize escalation or targeting.

### Falsification and threshold rules

Before reporting a relationship, reviewers must establish that:

- the cited source is authentic, accessible, and correctly represented;
- there is a specific, documented mechanism linking the records, rather than
  proximity, shared names, or association alone;
- plausible alternatives and missing data have been considered;
- the conclusion is no stronger than its evidence and method allow.

The supplied “10% Deviation Rule” is a proposed heuristic, not a validated
universal threshold. Any implementation must define the metric, denominator,
baseline period, uncertainty, missingness, and sensitivity to confounders.
Threshold crossings should prompt review, not imply misconduct.

## Output, privacy, and accountability

Permitted outputs should emphasize aggregate institutional processes, control
gaps, reporting delays, and evidence-quality limitations. Do not generate
guilt-by-association lists, public suspect rankings, victim-identifying
material, or sensational claims. Redactions and source-use restrictions must be
respected.

Reports should state:

- the question, scope, and intended audience;
- each source and its locator;
- the steps used to transform and compare source material;
- what is observed versus inferred;
- uncertainty, alternative explanations, and unexamined evidence;
- privacy and harm review outcomes;
- reviewer identity or role, dissent, and correction history;
- that legal or investigative determinations require qualified authorities.

No automated score or multi-reviewer agreement establishes guilt, legal
liability, causation, or the truth of a claim. Do not subpoena, contact,
confront, or otherwise take action against people based on model output.

## Validation and release criteria

The supplied case-study narrative is not validation evidence by itself.
Reproducible validation would require, at minimum:

1. a versioned and lawfully obtained source corpus with citations and access
   conditions;
2. published schemas, query logic, transformation code, and configuration,
   with secrets excluded;
3. a documented inclusion/exclusion and suppression log;
4. independent replication of calculations against cited primary materials;
5. false-positive, missing-data, and sensitivity analysis;
6. privacy, bias, security, and misuse review;
7. independent human review with recorded disagreement and correction paths.

Until these criteria are met, describe the pipeline as a conceptual
methodology, not as “validated,” “forensic,” or ready for operational
deployment.

## Repository implementation status

The repository currently contains a small evidence-recording prototype and a
Hatano–Nelson lattice module; it does not implement the AGLA-OSINT pipeline,
entity resolution, graph correlation, PHCA analysis, automated falsification,
distributed Council, or a case-study dataset.

- The FastAPI/Streamlit prototype records filenames, SHA-256 digests, and
  timestamps in SQLite. Uploads are hashed in memory and not retained; a later
  uploaded file can be compared with the recorded digests. This does not verify
  source authenticity.
- SQLite update/delete triggers protect ordinary SQL operations only. A person
  with database-file access can alter the database or its triggers, and
  well-formed record replacement is not detected by the basic startup checks.
  The SQLite file is not encrypted; this is not immutable forensic storage.
- The prototype requires a configured local API password and binds Docker
  Compose ports to loopback. It is still intended only for local use and is
  not suitable for public or shared deployment without additional controls.
- `core/lattice.py` implements the one-dimensional real-hopping
  Hatano–Nelson model. It is a numerical module and is not an OSINT anomaly
  detector or evidence validation method.

These are current code boundaries, not claims about future capability.

## Non-goals

- Automated accusation, suspect identification, or law-enforcement action.
- Individual-level scoring based on association or sensitive traits.
- Covert collection, access-control bypass, or surveillance of private people.
- Treating correlations, unexplained balances, model thresholds, or consensus
  as proof of intent or wrongdoing.
- Representing conceptual framework labels as implemented software features.
