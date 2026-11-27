Not sound. One critical: the three nightly region loads share one staging table, so they can wipe each other's rows and leave a region with no edges when the gritting planner runs at 03:00.

Top findings:

1. critical: `staging_edge`. At 01:00 all three loads run `DELETE FROM staging_edge` with no region filter (`loader/load_region.py` line 26). Whichever loader clears staging after another has staged its rows leaves that region with 0 edges. Reproduced in a scratch SQLite database: north ended with 0 edges. Fix: `DELETE FROM staging_edge WHERE region = ?`, and remove the lint ignore, whose reason does not hold for a shared table.
2. high: `load_region`. A failed validation keeps yesterday's rows for that region in `edge`, and nothing marks the region stale for the planner. Fix: a `load_status` table written in the swap transaction, checked by the planner, plus an alert on non-zero cron exit.
3. medium: `validate`. Two SELECTs per staged edge in Python, most of the 20 to 40 minute load. Fix: one set-based query per region with `NOT EXISTS`.
4. low: `node`. Nothing in these files writes to it, and validation depends on it. Question to confirm: where is it loaded?

Full report: `/run/work/docs/graph/ROAST.md`. Findings JSON: `/run/work/findings.json`.
