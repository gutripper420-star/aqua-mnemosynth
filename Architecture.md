# Architecture

## Design goal

The architecture separates representation, contextual analysis, inference, and accountability. Separating these concerns makes reasoning easier to inspect, test, revise, and explain.

## Logical layers

### 1. Symbolic representation

Stores explicit objects such as entities, claims, rules, observations, actions, and relationships.

Typical properties include:

- stable identifier;
- type;
- human-readable label;
- source or provenance;
- confidence or uncertainty;
- timestamps and revisions;
- links to related objects.

### 2. Context and PHCA analysis

Examines the environment in which an object or claim is interpreted. A representation may be reasonable in one context and unstable in another.

This layer should capture:

- active context;
- system phase or state;
- hierarchy and containment;
- transitions between phases;
- constraints and boundary conditions;
- signals that indicate instability or change.

The exact expansion of PHCA should be defined by the project before implementation. Until then, PHCA is treated as a configurable analytical model rather than a fixed acronym with an assumed meaning.

### 3. Recursive inference

Generates, evaluates, and revises hypotheses. Each inference should retain its inputs and reasoning trace rather than only returning a final answer.

A recursive cycle may be expressed as:

```text
observe -> represent -> hypothesize -> test -> revise -> compare
```

### 4. Risk and liability

Maps actions and decisions to possible harms, responsibilities, exposures, and mitigations. This layer must distinguish descriptive model output from legal conclusions.

### 5. Interface and audit trail

Provides human-readable reports, visualizations, exports, and a history of revisions. Every consequential output should be explainable back to its source objects and assumptions.

## Conceptual data flow

```text
Sources
  -> observations and claims
  -> symbolic graph
  -> context / PHCA state
  -> recursive hypotheses
  -> risk and responsibility analysis
  -> report, decision support, and audit trail
```

## Recommended implementation boundaries

A future codebase can be organized around these boundaries:

- `model`: schemas and domain objects;
- `context`: PHCA state and transitions;
- `inference`: hypothesis generation and evaluation;
- `risk`: exposure, impact, and responsibility analysis;
- `provenance`: sources, revisions, and evidence links;
- `reports`: human-readable output;
- `tests`: unit, integration, and scenario tests.

These are recommendations, not current directories in the repository.

## Invariants

A robust implementation should preserve the following invariants:

1. Every claim has a provenance status.
2. Every inference can identify its inputs.
3. Uncertainty is never silently converted into certainty.
4. Revisions do not erase prior reasoning history.
5. Risk scores, if introduced, expose their variables and limitations.
