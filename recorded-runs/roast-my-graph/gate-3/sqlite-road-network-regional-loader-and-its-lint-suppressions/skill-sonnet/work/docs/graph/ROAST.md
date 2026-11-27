# Roast: roadnet (sql/schema.sql, loader/, ops/crontab)

Verdict: One thing is critical and it is not subtle: three loaders start at 01:00 and share one `staging_edge` table that each of them empties completely, so on a normal night two of the three regions are replaced with nothing before the 03:00 gritting plan. Everything else is medium or sound.

Judged against:
- Engine: SQLite, WAL mode, `roadnet.db` on the planning server (README.md). Version: not stated.
- Row and edge counts: not stated.
- Batch: nightly load per region (north, south, west), each export replaces that region's rows in `edge` via `staging_edge`; a load takes 20 to 40 minutes, mostly validation (README.md).
- Concurrency: three cron entries at `0 1 * * *` start together and must all finish before crews are planned at 03:00 (README.md, ops/crontab).
- Interactive: the planner reads `edge` by `src` (`NEIGHBOURS` in loader/routes.py); a dashboard counts edges per region once a minute (`REGION_SIZE`).
- Invariants: edges go in only after validation; `PRAGMA foreign_keys = ON` is set by the loader (loader/load_region.py).

## Findings

### critical: `staging_edge`
Three loaders, one scratch table, and a DELETE with no WHERE. It is a relay race where every runner tackles the one in front.
Problem: When `load_region` runs for north, south and west at the same time (three `0 1 * * *` entries; each load takes 20 to 40 minutes), each run does `DELETE FROM staging_edge` with no region filter, which removes the rows the other regions staged. The lint suppression says "staging is scratch space, ours to clear", but the table is shared. A loader whose rows were wiped then validates zero rows (no problems found), runs `DELETE FROM edge WHERE region = ?` and inserts nothing. I replayed the three staging steps against an in-memory copy of sql/schema.sql with 3 edges per region: only the last region's rows were left in `staging_edge`, all three validations passed, and `edge` ended with west 3 rows, north 0, south 0. Which region survives depends on commit order.
Fix: Scope the clear to the region, which is the only change needed because validation, the swap and the final delete are already region-scoped: `con.execute("DELETE FROM staging_edge WHERE region = ?", (region,))`, and delete the `# lint: ignore SQL-DEL-001` comment, since the scoped statement no longer needs it. Add a guard before the swap so an empty or partial stage cannot pass: count the staged rows for the region and `raise SystemExit` unless the count equals `len(rows)`. Migration: run `DELETE FROM staging_edge;` once before the next night, and restore north and south `edge` rows from the last good export if the damage has already happened.

### medium: `validate`
Two SELECTs per edge, from Python, one network-less round trip at a time. SQLite has joins; it has been waiting by the door.
Problem: When `validate` runs on a region export, it executes one `SELECT 1 FROM node ...` per endpoint, so two lookups per staged edge, and the README says validation is most of each 20 to 40 minute load. It is correct today (it fits inside the 01:00 to 03:00 window), but it is the application doing the database's job, and once the loads are made to run safely the same cost is what you would pay if they ever have to run one after another.
Fix: Check in set form, same rules and same messages:
```python
def validate(con, region):
    problems = [f"{s}->{d}: length {km}" for s, d, km in con.execute(
        "SELECT src, dst, km FROM staging_edge WHERE region = ?1 AND km <= 0", (region,))]
    problems += [f"{s}->{d}: node {n} not in {region}" for s, d, n in con.execute(
        "SELECT s.src, s.dst, s.src FROM staging_edge s WHERE s.region = ?1 "
        "AND NOT EXISTS (SELECT 1 FROM node n WHERE n.id = s.src AND n.region = ?1) "
        "UNION ALL "
        "SELECT s.src, s.dst, s.dst FROM staging_edge s WHERE s.region = ?1 "
        "AND NOT EXISTS (SELECT 1 FROM node n WHERE n.id = s.dst AND n.region = ?1)", (region,))]
    return problems
```
Both lookups into `node` use its primary key. Compare the problem list with the old function on a past export before switching.

## Holds up
- `edge` primary key `(src, dst)`: `NEIGHBOURS` filters on `src`, the leading column, so the planner's lookup is an index search. It would not serve a lookup by `dst`; nothing in the files does one.
- `edge_region`: serves `REGION_SIZE` and the per-region `DELETE` in the loader. The dashboard runs once a minute, so even that count is fine.
- `edge.region` copying the region of its nodes: it serves the per-region replace the README describes, and the loader's validation (both ends must be in the region) is what keeps it in step. Only the loader writes `edge`.
- The swap in `load_region` (delete the region, insert from staging, clear staging, in one `with con:` transaction): readers in WAL mode see either the old region or the new one, and a failure rolls back to the old rows. Validation runs outside the write transaction, so the write lock is held briefly.
- `PRAGMA foreign_keys = ON` in `main`: the loader is the only writer in the files and it sets it, so the `REFERENCES node(id)` guarantee holds for its writes.
- `timeout=60` on the connection: three writers queue on the SQLite write lock for short transactions, which is enough.

## Not checked
- Nothing was run against a real `roadnet.db` or a real export (none in the repo), so plans and timings are unverified; the staging collision was replayed on an in-memory copy of the schema using the repo's SQL.
- SQLite version, row counts and edge counts are not stated.
- Whether an export can contain a repeated `(src, dst)` pair: `staging_edge` has no key, and the swap would then fail on `edge`'s primary key. It rolls back to the old rows, so it is loud, but it would leave that region stale; confirm whether the authority guarantees uniqueness.
- Whether road direction in the export covers two-way roads (both `src, dst` and `dst, src`); the files do not say.
- Who reads `log/*.log` before 03:00; nothing in the files alerts on a failed load.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
