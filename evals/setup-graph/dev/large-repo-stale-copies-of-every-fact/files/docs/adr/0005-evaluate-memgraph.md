# ADR 5: Evaluate Memgraph for the loans dashboard

Status: rejected (2025)

## Context

The loans dashboard runs the same six queries every few seconds. Memgraph's in-memory engine would make them
faster.

## Decision

Not now. The dashboard is fast enough after adding two indexes, and running a second engine for one screen is
not worth it. We stay on Neo4j for everything.

## If we revisit

Start from `queries/on_loan_now.cypher`; it is the only query on that screen that takes more than a few
milliseconds.
