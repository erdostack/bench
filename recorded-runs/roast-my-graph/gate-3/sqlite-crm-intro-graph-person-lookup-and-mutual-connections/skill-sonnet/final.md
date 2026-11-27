Nothing critical, but there is one high finding, and you are right that the graph part is innocent. `mutual_connections.sql` is two primary-key searches and took 0.15 ms for the most connected person in the sample.

The latency is in the step before it. `person_by_email.sql` does `WHERE lower(email) = lower(:email)`. The `UNIQUE` on `email` is case-sensitive, so the plan is `SCAN person`: all 1.2 million people on every sidebar request. On the 60,000-row sample the scan takes 16 to 22 ms, against 0.07 ms for an exact lookup. At 20 times the rows the 80 ms p95 cannot hold. The results are right, just slow.

Findings (also in `findings.json`, full write-up in `docs/graph/ROAST.md`):

1. `person_by_email.sql` (high): add `CREATE UNIQUE INDEX person_email_lower ON person (lower(email));` and leave the query alone. On a copy the plan became a `SEARCH` on that index and the lookup dropped to about 0.002 ms. Check production for case-only duplicate emails first (the query is in the write-up), and use a plain `CREATE INDEX` if there are any.
2. `email` (low, a question): `UNIQUE` is exact-spelling only, so if production holds two emails differing only in case, `fetchone()` picks one arbitrarily. The sample has none, and the unique index above enforces it.

Holds up: `mutual_connections.sql` and the `knows` key, `team_by_name.sql` (30 rows, rare admin page) and the two-statement API.

Not checked: production timings (the 20x scale comes from row counts and the sample's timings on this machine), and the loader that writes `knows` in both directions, which is not in the repo.
