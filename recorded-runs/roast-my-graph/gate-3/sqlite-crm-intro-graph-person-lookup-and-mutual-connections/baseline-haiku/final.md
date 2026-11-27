introgate: the graph is innocent, the email lookup is the problem

Your read is right. The mutual-connections query uses the primary key on knows at both hops and ran in about 0.02 ms per call on the sample. The graph is not what is blowing the 80 ms budget. The culprit is the lookup that runs first on every sidebar request.

person_by_email.sql filters on lower(email) = lower(:email). Wrapping the column in lower() means SQLite cannot use the UNIQUE index on email, so it scans the whole person table (EXPLAIN QUERY PLAN shows SCAN person). On the 60,000-person sample a lookup takes about 11.5 ms. Scanning is linear, so at 1.2 million people the same lookup is roughly 20 times slower, about 230 ms on this machine. That is already over the p95 budget before the graph query runs.

The fix is one index. A unique index on lower(email) makes the same query an index search. On an in-memory copy of intro.db the plan became SEARCH person USING INDEX, and the lookup dropped to about 0.004 ms. Check production for case-only duplicates before you create it. The sample has none.

Ranked list (full detail in findings.json):

1. person_by_email.sql (critical): add CREATE UNIQUE INDEX person_lower_email ON person (lower(email)). If production uses a different engine, use its functional-index syntax.
2. email (high): the UNIQUE constraint is case-sensitive, and 17,846 of the 60,000 sample rows have uppercase letters. Two case variants of one address can both be stored. Replace it with the lowercase index above, or store a normalized email column.
3. knows (medium): every relationship is stored in both directions, and the query relies on that without any check. One-way rows would silently drop connections. Enforce symmetry in the loader and add a nightly count of one-way rows.
4. mutual_connections.sql (low): leave the query alone. Add a tie-breaker to the ORDER BY so equal scores come back in a stable order, and check the degree distribution in production, since the query probes every contact of the rep.
5. team_by_name.sql (low): same function-on-column pattern, harmless with 30 teams, and not on the sidebar path.
6. api/sidebar.py (low): two round trips per request. Optional to merge once the index is in place.

Limits: intro.db is a 60,000-person sample, so the 230 ms figure is an extrapolation from linear scaling, not a production measurement. I confirmed the index effect on an in-memory copy and did not change intro.db.
