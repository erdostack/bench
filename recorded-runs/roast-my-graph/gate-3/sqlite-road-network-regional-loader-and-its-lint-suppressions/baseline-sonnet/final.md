Roasted roadnet (sql/, loader/, ops/). Findings are also saved in findings.json in the repo root (10 items).

The one to fix before January:

1. Critical: the three regional loads can wipe each other's data. All three cron entries start at 01:00 and share one `staging_edge` table. Each loader begins with an unscoped `DELETE FROM staging_edge`, so a later-starting loader deletes the rows another region has just staged. The victim's `validate()` then sees nothing, passes, and the swap deletes that region's rows from `edge` and inserts none. You can wake up to an empty north, south or west network, and the log will say nothing is wrong. The lint suppression on that line ("ours to clear") is wrong, because staging is shared. Fix: scope the delete to the region (or use per-region staging), remove the suppression, and stagger or serialise the loads with flock.
2. Critical: there is no sanity check on the export. An empty or truncated CSV passes validation and replaces the region's edges with nothing or a fragment. Refuse the swap if the staged count is 0 or drops sharply against the current count.
3. High: cron only writes to log files. If a load fails, the old data stays and nobody finds out before the 03:00 planning run. Add alerting on non-zero exit, a check that each region loaded tonight, and log rotation.
4. Medium: `validate()` runs two SQL queries per edge from Python, which is why a load takes 20 to 40 minutes. Do it as set-based SQL joins and it should take seconds. It does not catch infinite km values either.
5. Medium: validation requires both endpoints in the region being loaded, so roads that cross a region boundary are rejected or dropped, and the network is split at region borders. Decide who owns boundary edges.
6. Medium: `edge.region` has no CHECK, so a mistyped region value would never be cleaned up by the swap. The key `(src, dst)` also forbids parallel edges and doesn't flag duplicate rows in an export until the insert fails.
7. Low: `staging_edge` has no keys, and failed runs leave rows behind. Nothing here loads `node`, and `foreign_keys` is only enabled in the loader's connection. `REGION_SIZE` is not used anywhere in this repo, so its suppression reason cannot be checked.

I only read the code and did not run the loader. The concurrency failure depends on timing, but with simultaneous starts it is likely.
