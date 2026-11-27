# Roast: roadnet (sql/, loader/, ops/)

Verdict: Not sound. One critical: the three nightly region loads share one staging table, so they can wipe each other's rows and leave a region with no edges when the gritting planner runs at 03:00. Fix that before January.

Judged against:
- Engine: SQLite in WAL mode on the planning server, `roadnet.db` (README). Engine version: not stated.
- Regions: north, south, west, one export each (README, `ops/crontab`).
- Schedule: all three loads start at 01:00 together; each takes 20 to 40 minutes, most of it validation; planning starts at 03:00 (README, `ops/crontab`).
- Interactive reads: `NEIGHBOURS` per node, from the planner (`loader/routes.py`). Rare: `REGION_SIZE`, a once-a-minute dashboard query (`loader/routes.py`).
- Row counts and export size: not stated.
- Writers: one loader process per region, nightly (`ops/crontab`).

## Findings

### critical: `staging_edge`
Three loaders walk into one staging table and one of them comes out with nothing. Reproduced in a scratch database: north ends with 0 edges.
Problem: At 01:00 all three loads run `DELETE FROM staging_edge` with no region filter (`loader/load_region.py` line 26). When south clears staging after north has staged its rows, north's validation sees nothing and passes, and the swap leaves north with 0 edges.
Fix: Change line 26 to `DELETE FROM staging_edge WHERE region = ?` and pass the region. Remove `# lint: ignore SQL-DEL-001`, because its reason ("ours to clear") does not hold for a table shared by three loaders.

### high: `load_region`
A failed load leaves yesterday's network in place and nothing says so. Stale, but read as current.
Problem: When `validate()` returns problems, `load_region` raises `SystemExit` before the swap, so `edge` keeps the previous night's rows for that region. Nothing records the failure, and the planner reads `edge` at 03:00 as current.
Fix: Add a `load_status` table (`region`, `loaded_at`, `ok`). Write it in the same transaction as the swap, and write a failed row when validation fails. The planner refuses or flags any region whose latest status is not a successful load from the current night. Make the cron entries alert on a non-zero exit.

### medium: `validate`
The database's join is being done one row at a time in Python.
Problem: `validate()` runs two `SELECT`s against `node` for every staged edge. The README says validation is most of the 20 to 40 minute load, which holds the window in which `staging_edge` is in use open for longer.
Fix: Replace the loop with one set-based query per region:
`SELECT s.src, s.dst, s.km FROM staging_edge s WHERE s.region = ? AND (s.km <= 0 OR NOT EXISTS (SELECT 1 FROM node n WHERE n.id = s.src AND n.region = s.region) OR NOT EXISTS (SELECT 1 FROM node n WHERE n.id = s.dst AND n.region = s.region))`
Format the returned rows into the same error text. Time it on a real export; the engine version and row counts are not stated.

### low: `node`
Question to confirm: who fills `node`?
Problem: Nothing in `sql/schema.sql`, `loader/` or `ops/` writes to `node`, yet `validate()` and the `edge` foreign keys depend on it. If `node` is empty, every load fails validation.
Fix: Confirm where `node` is loaded and whether that runs before 01:00. Document it in the README next to the nightly load, and add a check that each region has node rows before validation starts.

## Holds up
- `edge` swap (`loader/load_region.py`, second transaction): the delete and insert run in one transaction, so readers see either the old or the new region. Would change if the planner needed a partial load.
- `edge` primary key `(src, dst)`: serves `NEIGHBOURS` (`loader/routes.py`), which filters on `src` first. Would change if the planner needed reverse neighbours, which would need an index on `dst`.
- `edge_region` index (`sql/schema.sql`): serves `DELETE FROM edge WHERE region = ?` and `REGION_SIZE`. Would change if region-level queries got much more frequent.
- `REGION_SIZE` lint ignore (`loader/routes.py`): a once-a-minute dashboard query over an indexed column. Sound.
- `PRAGMA journal_mode = WAL` with `timeout=60` (`sql/schema.sql`, `loader/load_region.py`): readers do not block the loaders, and a short wait for the write lock is allowed. Would change if writes lasted longer than 60 seconds.

## Not checked
- No `roadnet.db` is in the repo, so no plans or timings were run against real data.
- The critical race was reproduced in a scratch database (SQLite 3.53.1) by forcing the interleaving in order, not by running three processes at the same time.
- The SQLite version the planning server runs is not stated, so the fix assumes plain SQL that has been valid in SQLite for years.
- Where `node` is populated, and the export file format beyond the `from`, `to` and `km` columns, are outside these files.
- The CI linter's rule set was not available, so the lint suppressions were judged on their written reasons only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
