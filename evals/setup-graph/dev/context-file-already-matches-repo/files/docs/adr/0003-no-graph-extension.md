# ADR 0003: no graph extension

Status: accepted

## Context

The prerequisite data is a small directed acyclic graph (a few hundred courses). We looked at adding Apache AGE
to the database so that traversals could be written in Cypher, and at moving the data to a dedicated graph
database.

## Decision

Neither. Plain tables and recursive CTEs. The registrar's office already runs PostgreSQL and reads SQL; nobody
there reads Cypher, and the deepest chain in the catalogue is six courses.

## Consequences

Traversal queries are longer than their Cypher equivalents. Cycle protection is a depth cap in each CTE plus a
trigger that rejects a prerequisite which would close a loop.
