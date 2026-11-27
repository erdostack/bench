**The risk page spins because `queries/upstream_tiers.sql` never terminates on a graph with loops. Your README says this graph has plenty of loops.**

The recursive CTE `upstream` carries the full `path` array in every row. `UNION` only drops rows that are identical in all columns. `tier` and `path` differ on every revisit, so the dedup never fires and the recursion keeps going around each loop. The `DISTINCT ON (u.company_id)` at the end only runs after the CTE has finished. It stays fast for plants whose upstream has no loops, which fits "sometimes". `app/risk_page.py` has no `statement_timeout`, so the query runs until someone kills the connection.

I reproduced it on a local PostgreSQL 16.15 with a random graph of 14,000 companies and about 95,000 links:

- **Original query:** still running when a 15 s timeout cancelled it.
- **Adding a cycle guard** (`s.supplier_id <> ALL(u.path)`) also hit the timeout. It still enumerates every simple path, which is exponential.
- **Fix that worked:** a tier-bounded breadth-first walk. It carries one parent per row, picks the lowest tier per company with `DISTINCT ON`, and rebuilds the breadcrumb by walking the parents. It returned 13,981 rows in about 2.7 s. The full query is in `findings.json`.

**Findings (5 in `findings.json`):**

- **Critical:** `queries/upstream_tiers.sql`, the path-carrying CTE described above. Replace it with the breadth-first version.
- **High:** `app/risk_page.py` has no query timeout. Add `SET LOCAL statement_timeout` and handle the cancel with a degraded page. Consider caching per plant, since buyers open it often.
- **Medium:** the recursion has no depth cap. It also returns the plant as upstream of itself when a loop leads back to it. The fixed query excludes it.
- **Low:** `.replace("$1", ...)` on the whole SQL file is fragile.
- **Low:** `docker-compose.yml` publishes Postgres on all interfaces with a fixed password and no `statement_timeout`.

**Caveats:**

- I tested on synthetic data, not your real graph. Set the 12-tier cap in the fix above the deepest real supply chain.
- 2.7 s per page open is still slow for something buyers open many times a day, so cache it.
- The schema and indexes are fine. The primary key already serves the traversal.
