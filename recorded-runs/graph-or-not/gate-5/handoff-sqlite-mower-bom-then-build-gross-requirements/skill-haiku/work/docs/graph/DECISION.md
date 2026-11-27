# Graph decision

Decision: recursive-sql

Gross requirements for an order of N mowers are a walk down a BOM of at most 11 levels, multiplying each line's quantity by 1.04 for scrap and summing per bought-in part, which Postgres already does with one recursive query. The user measured 0.4 s on a copy for the biggest ride-on mower against a 3 s budget, and my own timings on SQLite put it at a few milliseconds per root, so the walk fits; the consultant's graph database would add a second store to a system that already meets the need.

## Workload facts

- Items: 48,000 (stated by the user)
- BOM lines: 210,000 (stated by the user; `db/schema.sql` holds the `bom_line` table)
- Deepest BOM: 11 levels (stated by the user); the walk must stop at depth 11
- Runs: about 300 gross-requirement runs a day (stated by the user), so 300 x 0.4 s = 120 s of database time per day (derived from the user's timing below)
- Latency budget: under 3 seconds per run (stated by the user), so 0.4 s is about 13% of budget, about 7.5 times headroom
- Measured by the user: a recursive query on a copy of the Postgres database for the biggest ride-on mower returned in 0.4 s (stated by the user; not re-run here, since no Postgres server is available in this environment; the `psql` client exists but no server)
- Production engine: Postgres 16 (`README.md`); tests run on SQLite (`README.md`)
- Scrap rule, as the planning lead states it: 4% on every BOM line, so a path's multiplier is 1.04 for each line on it, and a part three levels down gets the factor three times (stated by the user). The line multiplier is therefore `qty_per x 1.04`, which the walk carries down each path.
- Schema: `bom_line (parent_id, component_id, qty_per)` with primary key `(parent_id, component_id)`, which serves lookups by parent, and index `bom_line_component (component_id)` (`db/schema.sql`)
- Query runner: `planning/sqlfile.py` passes named parameters as a dict to `cursor.execute` and the SQL files use `:name` placeholders (`planning/sqlfile.py`, `sql/*.sql`). `:name` is SQLite's syntax; psycopg expects `%(name)s`. The README requires each query to work on both engines, so the Postgres path for the new query needs checking (unverified here, since no Postgres server is available).
- Measured, synthetic on SQLite 3.53.1 (generator in scratch, not the real BOM; 48,000 items; two shapes: A with 20% made items and up to 49 children per parent, B with 40% made items and up to 23 children per parent; rejection sampling gave 203,650 and 207,114 lines rather than 210,000): the naive recursive walk with the scrap factor, one row per path to depth 11, took 21.4 ms (A) and 23.4 ms (B) for the three largest roots by path count, and 1.6 ms and 1.4 ms per root for 30 random made roots (measured, `WITH RECURSIVE` with `UNION ALL`, one statement per root)
- Measured, synthetic: paths to depth 11 for the largest roots were 3,624 (A) and 2,964 (B), against 3,147 and 2,840 distinct nodes reached; the path rows and the distinct nodes are close, so the walk repeats little work in these shapes (measured)
- Measured: the naive path-row sum and a per-level sum agree on a 600-item DAG (max difference 0.0 once the root's own depth-0 row is excluded; with the root included the difference is exactly the root's 1.0) (measured, SQLite 3.53.1)
- Measured but not used: a per-level loop in Python with a temporary table took 1.1 to 3.4 s per root in this harness; that number reflects the harness, not the database, and is not a reason to choose a graph store
- unknown: the real path count and distinct-node count on the Postgres copy (only one timing was given); whether the 0.4 s run was warm or cold; whether the biggest ride-on mower is the worst case by path count rather than by size; whether the scrap also applies to the works order's own top-level line (not stated); how many runs can overlap at peak (not stated); the Postgres version of the copy beyond the README's 16

## Options considered

- graph-database (a dedicated graph store, the consultant's proposal): rejected, because the walk is bounded at 11 levels and measured at 0.4 s on Postgres against a 3 s budget; a second store would need a nightly copy from PLM alongside the existing one, and the computation is a product along each path summed per part, which SQL does in one statement
- in-process-library (the BOM loaded into memory with a graph library): passed over, because recursive-sql holds at the rung before it; 48,000 items and about 210,000 lines are small enough to hold in memory (estimate, not measured here), so this is the fallback if the real Postgres measurement fails the budget
- recursive-sql (recursive queries on the Postgres database already run): chosen, because the walk is from one starting item to a fixed depth of 11, the database is already operated, and the measured cost is 0.4 s against a 3 s budget on the user's measurement and a few milliseconds per root on the synthetic data
- no-graph (plain joins, no traversal): rejected, because the requirement follows the BOM through up to 11 levels, which is a traversal of a relation between items of the same kind and not a join across one link table

## What would change the decision

- A BOM deeper than 11 levels, or a walk with no depth limit, would move this to in-process-library for the batch case and to graph-database only if it became an online request with a budget that SQL measured failing (the depth and the budget are set by the planning lead and the product owner, not by the repo)
- A measured time on the real Postgres copy over 3 seconds for the worst order (a percentile, or a failure rate with its total, not a single slow run) would move this to in-process-library, with the BOM held in memory and reloaded from the nightly PLM copy
- A requirement to recompute gross requirements for every open works order in one nightly batch would move this to in-process-library on a snapshot
- A change to the scrap rule that makes the factor depend on the part rather than the line would not change the option, since it is still a product along each path
- Trial before shipping: run the walk on the Postgres copy for the 10 largest assemblies by path count and 20 random ones, record time, path rows and distinct nodes, check that the root's depth-0 row is excluded, and confirm that the `sql/` file runs through `planning/sqlfile.py` on Postgres with psycopg's placeholder syntax
