# helpline-graph

Support desk graph: customers, tickets, agents and the messages on each ticket.

- Neo4j 2026.10.2 Enterprise in every environment (`deploy/neo4j.env`).
- `db/changes/`: numbered changes, applied in order on deploy by `deploy/apply-changes`, each statement
  as an auto-commit query.
- `queries/`: what the desk app runs.
- `docs/data.md`: sizes and retention.
