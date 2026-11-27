# Related objects (and trails later)

Decision: no-graph

## Workload facts (from the owner, 2026-11-23)

- "Related objects": the objects a curator linked to this one, one step (api/sql/related.sql).
- 120k objects, 900k curated relations, Postgres 16. About 60 object page views a second; 200 ms for the page.
- Agreed with Dana: if "trails" is funded (shortest chain of relations between two objects, up to 6 steps), the
  relations move into an in-memory graph in the API. Her prototype: all relations in 1.8 GB, a trail in 30 ms.
  Not a graph database even then (API hosts have 8 GB).

## Options considered

- graph-database (Dana's proposal): rejected for now and, by agreement, for trails too.
- in-process-library: the agreed route once trails is funded.
- recursive-sql: nothing recurses today.
- no-graph: chosen for related objects, a single indexed lookup.

## What would change the decision

- Trails being funded: switch to in-process-library (relations loaded into a graph in the API).
