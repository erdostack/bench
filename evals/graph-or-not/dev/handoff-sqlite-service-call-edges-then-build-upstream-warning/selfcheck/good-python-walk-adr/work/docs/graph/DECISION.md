# Upstream warning before a deploy

Decision: recursive-sql

## Workload facts (from the owner, 2026-11-23)

- `call_edge`: one row per caller, callee and UTC day, loaded nightly from tracing into the deploy tool's SQLite
  database; 90 days kept.
- 1,400 services, about 31,000 edges on a given day; call chains up to 11 deep.
- About 230 cycles (callbacks, webhooks, services calling each other): the walk must not go round them.
- Rule agreed with SRE: an edge counts only if it was seen on at least 3 of the last 7 days (one-off calls from
  backfills, load tests and debugging must not put a service on the warning).
- About 600 deploys a day; the warning has 2 seconds.

## Options considered

- graph-database (Ines's proposal): rejected. A server and a nightly load, for a walk over one week of edges.
- in-process-library: would work (31k edges), but the file already has the data and an index on callee.
- recursive-sql: chosen. Qualifying edges first (GROUP BY caller, callee over the 7 days, HAVING count of days
  >= 3), then a recursive walk from the service over callers with UNION, which ends on cycles.
- no-graph: no; "through other services" is transitive.

## What would change the decision

- Needing the path that makes a service upstream, or weighting by call volume, at interactive speed.
