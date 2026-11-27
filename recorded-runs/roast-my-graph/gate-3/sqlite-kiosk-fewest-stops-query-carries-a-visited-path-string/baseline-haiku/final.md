The slowness is almost certainly `queries/fewest_stops.sql`. The other two queries are fine.

**What's wrong**

- `fewest_stops.sql` is a recursive CTE that enumerates every simple path out of `:from_stop`, and only then applies `ORDER BY hops LIMIT 1`. On this 144-stop grid the number of paths explodes. Asking for stop 1 to stop 2 against the copy in `tram.db` did not finish in 60 seconds, and an unreachable pair would never finish. The comment says it "cannot loop", which is true, but avoiding loops is exactly what makes it exponential.
- `stops_within.sql` and `line_stops.sql` finish in well under a millisecond on the copy. `stops_within` is bounded by `:n`, so it is fine.
- `link_to` is an index no query uses. It is harmless but pointless.

**Fix**

- Replace `fewest_stops.sql` with a level-by-level breadth-first search that deduplicates on `(stop, hops)` with `UNION` and takes `MIN(hops)` for `:to_stop`, with a depth cap. I tested this against a Python BFS on 44 stop pairs, including 1 to 144 and 5 to 100: zero mismatches, about half a second in total.
- The new query drops the `path` column. If the kiosk shows the route and not just the count, carry a parent stop through the BFS.
- Drop `link_to` from `schema.sql`, unless a reverse-direction query is planned.

Findings are in `findings.json` in the repo root.
