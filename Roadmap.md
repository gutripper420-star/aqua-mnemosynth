# Roadmap

The roadmap is intentionally staged so that the project can grow from a documented concept into a testable system.

## Phase 0: Foundation

- Define the project vocabulary.
- Decide what PHCA means operationally in this project.
- Establish contribution, documentation, and versioning conventions.
- Add example scenarios and expected outputs.

## Phase 1: Domain model

- Define schemas for symbols, claims, evidence, assumptions, contexts, and hypotheses.
- Define provenance and revision records.
- Define validation rules and serialization format.
- Add fixtures for small symbolic graphs.

## Phase 2: Analysis engine

- Implement graph traversal and relationship queries.
- Implement context and phase transitions.
- Add hypothesis comparison and contradiction detection.
- Preserve reasoning traces for every inference.

## Phase 3: Risk modeling

- Define failure-mode and causal-chain schemas.
- Add transparent risk dimensions.
- Implement mitigation and residual-risk records.
- Add human review checkpoints.

## Phase 4: Interfaces and reports

- Create a command-line or API entry point.
- Generate readable analysis reports.
- Add graph and timeline visualizations.
- Provide export formats for audit and review.

## Phase 5: Validation

- Add unit and integration tests.
- Build scenario-based evaluations.
- Test ambiguous, contradictory, and incomplete inputs.
- Conduct security, privacy, bias, and misuse reviews.

## Definition of done for a feature

A feature is not complete until it has:

- a clear specification;
- implementation and tests;
- documentation and examples;
- error handling;
- provenance or audit behavior where relevant;
- known limitations;
- review by an appropriate maintainer.
