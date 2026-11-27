# Roast: introgate (schema.sql, queries/, api/)

Verdict: Nothing critical, but one high, and you were right that the graph part is innocent: the mutual-connections query is a pair of primary-key lookups. The latency is in the step before it. `person_by_email.sql` wraps the column in `lower()`, so the `UNIQUE` index on `email` cannot be used and every sidebar request scans all 1.2 million people. Add an index on `lower(email)`.

Judged against:
- SQLite; version not stated in the repo. Run read-only on the sample with SQLite 3.53.1 (python `sqlite3`) (README.md, intro.db).
- Production: 1.2 million people, 9 million `knows` rows, p95 budget 80 ms per sidebar request. `intro.db`: 60,000 people, 480,722 `knows` rows (README.md, intro.db).
- Every contact opened in the CRM calls the API: `person_by_email.sql`, then `mutual_connections.sql`. Emails arrive in whatever case the CRM stored them (README.md, api/sidebar.py).
- `knows` is stored in both directions, the loader writes a row each way (README.md). The loader is not in this repo.
- Admins pick one of 30 teams by name on the settings page (README.md).

## Findings

### high: `person_by_email.sql`
The database has a perfectly good index on `email` and the query politely declines to use it, on every sidebar open, out of what I can only call principle.
Problem: `WHERE lower(email) = lower(:email)` cannot use `sqlite_autoindex_person_1` (the `UNIQUE` on `email` is case-sensitive and indexes the raw text). Every sidebar request, which runs this first, reads every person row: `EXPLAIN QUERY PLAN` says `SCAN person`. At 1.2 million people that is 20 times the 60,000 rows of the sample, where the scan already takes 16 to 22 ms against 0.07 ms for an exact lookup, so the stated 80 ms p95 cannot hold at production size, whatever the planner does. Mixed-case emails are the normal case here (17,846 of 60,000 in the sample), which is why the query lowers both sides. Rated high, not critical: the result is right and the request finishes, it is only too slow for the budget.
Fix: `CREATE INDEX person_email_lower ON person (lower(email));` leaves the query as written; on a copy of intro.db the plan changed to `SEARCH person USING INDEX person_email_lower (<expr>=?)`, the same row came back, and the lookup took about 0.002 ms. Prefer the unique form `CREATE UNIQUE INDEX person_email_lower ON person (lower(email));`, which also closes the question under `email`; it fails if production has two emails that differ only in case, so check that first with `SELECT lower(email) FROM person GROUP BY 1 HAVING count(*) > 1;`. Expression indexes need SQLite 3.9 or later; verified on 3.53.1. On a 1.2 million row table, build it during a quiet period. Do not add a plain index on `email` or a second query path: neither serves `lower(email)`.

### low: `email`
Question to confirm: `email TEXT NOT NULL UNIQUE` is unique only by exact spelling, but the CRM matches it without regard to case. If production has `Ana@Globex.example` and `ana@globex.example` as two rows, `person_by_email.sql` returns both and `api/sidebar.py` takes `fetchone()`, an arbitrary one. The sample has none (0 groups of case-only duplicates in 60,000), so this is a question, not a defect.
Fix: The unique index in the fix above enforces it; otherwise, normalise to lower case on write and match with `=`.

## Holds up
- `mutual_connections.sql`: the plan is `SEARCH k1 USING PRIMARY KEY (a=?)`, `SEARCH k2 USING PRIMARY KEY (a=? AND b=?)`, `SEARCH p USING INTEGER PRIMARY KEY`, so each step is an index search with no scan. It took 0.15 ms for the most connected person in the sample (20 connections; production averages 7.5 per person, 9 million over 1.2 million). Because `knows` is stored in both directions, reading `k1.a = :me` is enough, and `CHECK (a <> b)` keeps `:me` and `:target` out of the results. It would change if one person had tens of thousands of connections, which nothing states.
- `knows`: the primary key `(a, b)` serves both lookups the query makes; the sample has no row without its reverse. What keeps the two directions in step is the loader, which is not in this repo.
- `team_by_name.sql`: `lower(name) = lower(:name)` scans `team`, which has 30 rows, on a rare admin page. A scan of 30 rows is not worth an index.
- `api/sidebar.py`: two statements per request, both single-row or primary-key reads; the cost is in the first statement, not in the number of round trips.

## Not checked
- Production was not available: no timings at 1.2 million rows. The 20x scale is from the row counts, and the 16 to 22 ms scan time is from the sample on this machine, not from prod.
- Whether production contains emails that differ only in case, and the loader that writes `knows` in both directions, are not in the repo.
- Request rate is not stated.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
