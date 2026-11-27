What's going on: the upstream query never terminates when the supply graph has a ring, and the page has no timeout to stop it.

**The cause is in `queries/upstream_tiers.sql`.** The recursive CTE carries `(company_id, tier, path)`, and `UNION` deduplicates on that whole row. Going once round a ring produces the same company with a higher tier and a longer path, which is a new row. So the recursion never reaches a fixed point. The README says the graph has rings, and buyers open the page many times a day, so the query runs away and holds a connection until something kills it. I reproduced the growth with the same recursion in SQLite on a two-company ring: the row count keeps climbing with each cap I set. I could not run it against PostgreSQL 16 here because no server is installed, so the PostgreSQL run is unverified, but the logic does not depend on the engine.

**It is also expensive without rings.** Each distinct path is its own row, so a supply network with shared suppliers grows the row count exponentially with depth, and each row copies its array. The `DISTINCT ON` only runs after all of those rows exist.

**Why it spins instead of failing.** `app/risk_page.py` sets no `statement_timeout`, and `docker-compose.yml` does not set one either. The default is no limit, so nothing ends the query until the connection is killed from outside.

**What to fix, in order:**
1. Rewrite the recursion over `(company_id, tier)` only, bound the depth, and take the minimum tier per company with `DISTINCT ON`. Build the breadcrumb from a BFS with parent pointers, not from paths carried through the recursion.
2. Add a regression test with a two-company ring.
3. Set a `statement_timeout` and an `idle_in_transaction_session_timeout` for the application role, so a bad query fails fast.
4. Cache results per plant, invalidated on writes to `supplies`, since the graph changes rarely.
5. Exclude the plant itself from its own upstream list, which a loop can put there.

The smaller items (the string-replaced `$1` placeholder and the note that rings are allowed) are in `findings.json` in the repo root.
