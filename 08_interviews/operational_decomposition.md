# Optional Operational Decomposition Exercise

Choose a real but non-confidential workflow you understand. Write a two-page design
that turns an ambiguous operation into explicit state and controlled actions.

## Model

- **Objects:** identities, required properties, ownership, lifecycle.
- **Links:** cardinality, direction, and what creates or removes them.
- **Actions:** preconditions, authorization, side effects, idempotency, undo path.
- **Permissions:** object-, property-, and action-level boundaries.
- **Invariants:** truths that must hold across partial failure.
- **Evaluation:** offline cases, shadow behavior, human review, production metrics.

## Failure exercise

Pick one irreversible or financially meaningful action. Trace duplicate delivery,
timeout after commit, stale input, partial downstream failure, and operator retry.
Design the idempotency key, audit record, reconciliation path, and escalation.

## Review test

A reader should be able to challenge the design without knowing a product-specific
vocabulary. If the explanation depends on “the AI handles it,” decompose further.

