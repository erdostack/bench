# ECO impact screen: where-used

Decision: in-process-library

## Workload facts (from the conversation of 2026-11-24)

- 95,000 items, 400,000 BOM lines; impact screen opened about 600 times a day; p95 180 ms.
- sql/where_used.sql already walks any depth and stops on PLM loops (path check).
- **Rule agreed with Ines (DBA): stay on this query while the impact screen's p95 is under 800 ms. Past 800 ms,
  move the walk into the ECO service's memory with networkx, not a graph database.** Ana's prototype: 350 MB,
  20 ms.

## Options considered

- graph-database (contractor): rejected, and ruled out by the rule above.
- in-process-library: the agreed next step once p95 passes 800 ms.
- recursive-sql: keep what is there. Nothing to change.
- no-graph: no, the walk is any depth.

## What would change the decision

- p95 of the impact screen above 800 ms: move to networkx in the ECO service.

## Update after the Ostrava merge

- 1.1M BOM lines; impact screen p95 1.3 s, past the 800 ms line. Moving the walk to networkx in the ECO service.
