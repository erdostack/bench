# Circuit trace

Decision: graph-database

## Workload facts (from the conversation, 2026-11-23)

- 28 harness variants; biggest: 9,400 pins and splices, 14,000 wires.
- viewer/trace.py: one query per pin reached; ~600 queries and 2.1 s for a trace on the biggest variant.
- networkx: 90 ms to load the biggest variant, 45 MB, 0.4 ms per trace.
- Data changes only at the monthly engineering release. Viewer: two containers, 512 MB each.

## Options considered

- graph-database: rejected; a server and a monthly load for a 45 MB graph traced in 0.4 ms.
- in-process-library: chosen; load each variant on first use, keep it until the next release.
- recursive-sql: one round trip instead of 600 would also help; networkx is simpler and faster here.
- no-graph: rejected; a trace is a connected-component walk.

## What would change the decision

- Live editing of harnesses by many designers at once, with traces over unreleased changes.
