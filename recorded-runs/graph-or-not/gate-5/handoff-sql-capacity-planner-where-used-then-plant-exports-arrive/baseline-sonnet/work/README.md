# capaplan

Capacity planning for the Linz plant: re-times works orders when components change.

- Python 3.12, Postgres 16. Tests use a SQLite file built from `db/schema.sql`.
- `capaplan/run.py` is the planning run, started by the scheduler; `sql/` holds its queries, which have to work
  on Postgres and SQLite.
- BOMs are copied from PLM every night.

## Where-used decision

Recursive SQL, one set-based query per run (`sql/where_used_batch.sql`, used by `affected_assemblies()` in
`capaplan/run.py`). No graph database. The BOMs are not loaded into the planner.

- All three plants are 1.2M BOM lines. A synthetic layered BOM of about 1.05M lines, 40,000 changed components,
  ran the batch query in about 10 s on SQLite (not Postgres, not real data).
- The networkx option was measured on a test host: 1.4 GB resident against the 2 GB the planner gets, and 3 min
  for the 40,000 where-used queries. It fits the 10-minute limit but leaves little memory headroom, so it is the
  fallback, not the plan.
- Before go-live, time the batch query on a Postgres copy of all three plants. If it takes more than about 5
  minutes, switch to the in-process option.
