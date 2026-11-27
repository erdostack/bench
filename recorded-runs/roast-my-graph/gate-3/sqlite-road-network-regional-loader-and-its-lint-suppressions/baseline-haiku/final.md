Roadnet review (sql/, loader/, ops/). Findings are saved in work/findings.json, 12 entries.

The one to fix before January: the three nightly loads race on a shared staging table. load_region() runs an unscoped DELETE FROM staging_edge, and all three cron entries start at 01:00 against the same roadnet.db. If one region's staging rows are wiped by another region's run, that region's live edges are deleted and nothing is inserted. The run still exits 0, and the planner routes that region with no roads. The lint suppression SQL-DEL-001 is hiding this statement.

Also high:
- An empty or truncated export passes validation (zero rows, zero problems) and wipes the region. Nothing compares the new row count with the old one.
- A failed load is silent. Cron output goes only to log files, with no alert, and the planner runs at 03:00 on last week's network.

Medium: validation runs two SELECTs per edge in Python, which is most of the 20 to 40 minutes. It also misses NaN and inf lengths. The loader never writes node, so validation depends on data this repo does not manage. The (src, dst) primary key has no region, and validation rejects cross-region endpoints, so border segments may not load at all. I could not confirm that against real export data. Edge has no CHECK constraints. Export parsing gives poor errors.

Low: schema.sql is not applied by any repo code, REGION_SIZE's "dashboard only" suppression sits in the planner's query module, and the logs are never rotated.

Things I could not check from the repo: the CI lint rules, where node is populated, and the authority's export format.
