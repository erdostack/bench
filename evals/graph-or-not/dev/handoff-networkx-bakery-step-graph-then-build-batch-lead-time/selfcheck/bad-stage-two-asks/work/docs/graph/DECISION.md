# Batch lead time

Decision: in-process-library

## Workload facts

- 1,800 recipes, about 26 steps each, one SQLite file; about 150 screen opens a morning.

## Options considered

- graph-database: rejected. in-process-library: chosen. recursive-sql: possible. no-graph: no.

## What would change the decision

- Oven and mixer capacity entering the lead time.
