# Risk and Liability Model

## Purpose

The risk and liability layer helps identify where a system can fail, who may be affected, and which controls could reduce exposure. It is decision support, not a substitute for legal advice or formal compliance review.

## Risk dimensions

A future implementation may evaluate risk across several dimensions:

- **Impact:** severity of possible harm.
- **Likelihood:** estimated chance of occurrence.
- **Exposure:** degree to which an actor or system is connected to the outcome.
- **Control:** ability to prevent, detect, or correct the outcome.
- **Foreseeability:** whether the failure could reasonably have been anticipated.
- **Reversibility:** how easily the harm can be undone.
- **Distribution:** how benefits and harms are distributed among parties.

These dimensions should remain visible rather than being hidden inside one unexplained score.

## Causal responsibility

Responsibility analysis should distinguish among:

- initiating an action;
- approving or directing an action;
- providing a necessary dependency;
- failing to monitor or intervene;
- benefiting from an outcome;
- being affected without meaningful control.

A causal connection alone does not establish legal liability. The model should present relationships and uncertainties for qualified human review.

## Failure analysis

For each significant failure mode, record:

1. trigger or initiating condition;
2. affected component or party;
3. immediate outcome;
4. downstream consequences;
5. existing controls;
6. control gaps;
7. detection signals;
8. mitigation or recovery plan;
9. residual uncertainty.

## Mitigation hierarchy

Prefer mitigations in this order:

1. eliminate the hazardous condition;
2. reduce the likelihood through design;
3. detect the condition early;
4. limit the impact;
5. provide recovery and accountability;
6. document residual risk and obtain appropriate approval.

## Ethical safeguards

The project should avoid automated blame assignment, unsupported legal conclusions, discriminatory proxies, and recommendations that conceal tradeoffs. Models affecting people should be reviewed by domain experts and impacted stakeholders.

## Example output language

Good: “The current evidence suggests a potential control gap at the approval stage; additional records are needed before assigning responsibility.”

Avoid: “The system proves that person X is liable.”
