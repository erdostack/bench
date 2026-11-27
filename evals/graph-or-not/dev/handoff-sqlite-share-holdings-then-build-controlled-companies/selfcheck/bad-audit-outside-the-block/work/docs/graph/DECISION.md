# Controlled companies panel on the client page

Decision: recursive-sql

## Workload facts (given by the owner, 2026-11-23)

- Control, for this panel, is a stake of 25% or more at every step of the chain (compliance's definition, from
  Sigrid; not the legal majority).
- 2.1M companies, 3.4M holdings. The longest control chain found is 9 companies.
- Cross-holdings exist: about 1,100 holdings close a loop (mutual stakes or longer rings). The registry feed does
  not prevent them.
- The client page is opened about 2,500 times a day; the panel may take up to 2 s.
- Measured: a recursive query on a replica for the largest client group, 140 ms.

## Options considered

- graph-database (Neha's proposal): rejected. A second copy of the registry to load nightly, for a lookup the
  database answers in 140 ms out of 2 s.
- in-process-library: rejected. 3.4M holdings in the web app to read a few dozen per page view.
- recursive-sql: chosen. One recursive query over `holding`, pct >= 25, carrying the path so loops end.
- no-graph: rejected. Control passes through chains of up to 9 companies.

## What would change the decision

- The panel missing its 2 s on Postgres with the query above.
- Compliance changing the definition to something the walk cannot express (aggregated stakes across branches).
