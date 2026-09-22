# Core Concepts

## Symbol

A symbol is an explicit representation of an entity, property, action, claim, relation, or transformation. Symbols are useful because they make otherwise implicit reasoning inspectable.

## Claim

A claim is a proposition that may be supported, challenged, unresolved, or rejected. A claim is not the same as evidence: evidence is what informs its evaluation.

## Evidence

Evidence is an observation, source, measurement, record, or argument that bears on a claim. Evidence should include provenance and a description of its limitations.

## Assumption

An assumption is a condition accepted temporarily so that analysis can proceed. Assumptions must be visible and testable; hidden assumptions are a major source of model failure.

## Context

Context is the set of conditions that influence how an object, claim, or action should be interpreted. Context may include time, actors, environment, constraints, and system state.

## PHCA state

A PHCA state is a structured snapshot of the contextual or phase-related conditions used by the project’s PHCA analysis. The implementation should define its fields, allowed transitions, and validation rules explicitly.

## Hypothesis

A hypothesis is a candidate explanation or interpretation. Multiple hypotheses should be allowed to coexist when evidence does not justify premature selection.

## Recursive inference

Recursive inference is the repeated refinement of hypotheses as new evidence, constraints, or counterarguments are introduced. Each cycle should preserve what changed and why.

## Counterfactual

A counterfactual asks what might happen if a relevant condition were changed. Counterfactuals are useful for finding causal dependencies and testing the stability of a conclusion.

## Causal chain

A causal chain is an ordered or branching sequence connecting conditions, actions, events, and outcomes. It is the primary structure for tracing effects and responsibility.

## Liability surface

A liability surface is a set of points where decisions, omissions, controls, or dependencies may create exposure or responsibility. It is an analytical concept, not an automatic legal determination.

## Provenance

Provenance records where a piece of information came from, when it was observed, how it was transformed, and who or what modified it.

## Reasoning trace

A reasoning trace is the inspectable record connecting inputs, transformations, intermediate hypotheses, and outputs. It is essential for review and debugging.

## Uncertainty

Uncertainty represents incomplete information, ambiguity, disagreement, measurement limits, or model limitations. It should be represented directly rather than hidden inside a single confidence number.
