# Roast: tram kiosk database (schema.sql, queries/fewest_stops.sql, queries/stops_within.sql, queries/line_stops.sql)

Verdict: One thing is wrong and it is the whole answer: `queries/fewest_stops.sql` walks every possible route through the grid instead of the shortest one, so "How many stops to X?" does not finish. The schema and the other two queries are fine.

Judged against:
- SQLite, local copy `tram.db` rebuilt nightly from `schema.sql` (README.md). Version of the kiosk engine: not stated; checks here ran on SQLite 3.53.1.
- 144 stops, 420 directed links (every link stored both ways), twelve lines crossing in a grid, "so there are many ways round" (README.md; counts confirmed in tram.db).
- Interactive: shortest-stops question, nearby stops with n = 1 or 2, a line's stops (README.md). Writes: nightly refresh only.

## Findings

### critical: `queries/fewest_stops.sql`
Somebody asked the database for the shortest way across town and it replied by walking every way across town. Twelve crossing lines, 144 stops, and a path string that remembers each trip so nothing is ever shared. The kiosk is not slow, it is on a pilgrimage.
Problem: When a kiosk asks "How many stops to X?" on this grid network, the recursive CTE `walk` carries a `path` and only avoids revisiting a stop within the same path, so it generates every simple path from the start stop. In tram.db a capped copy of `walk` hit 2,000,000 rows from stop 1 without finishing, and the full query was interrupted after 20 s even for a destination one link away. `ORDER BY hops LIMIT 1` runs after all those rows exist.
Fix: Keep one row per stop and hop count, stop at the target, bound the depth (SQLite 3.53.1, checked):
```sql
WITH RECURSIVE walk(stop, hops) AS (
  SELECT :from_stop, 0
  UNION
  SELECT l.to_stop, walk.hops + 1
  FROM walk JOIN link l ON l.from_stop = walk.stop
  WHERE walk.stop <> :to_stop AND walk.hops < 143
)
SELECT MIN(hops) AS hops FROM walk WHERE stop = :to_stop;
```
Roughly 30 ms for the farthest pair (22 hops), and identical to a breadth-first search for all targets from three start stops. This returns the count, which is what the kiosk question asks. If the route itself is needed, do not carry a path string through the recursion: look the route up afterwards or rebuild it in the application.

### low: `link_to`
An index nobody invited. Nothing queries link by `to_stop`, so it just gets rebuilt every night.
Problem: `fewest_stops.sql`, `stops_within.sql` and `line_stops.sql` all filter on `from_stop` or `line`; none uses `link_to`.
Fix: `DROP INDEX link_to;` unless a reverse lookup is added.

## Holds up
- `link` primary key `(from_stop, to_stop)` WITHOUT ROWID: serves every `from_stop` lookup in the recursive queries (plan: SEARCH l USING PRIMARY KEY). Both directions are stored, so the walk needs no reverse index.
- `link_line`: `queries/line_stops.sql` searches it (SEARCH l USING COVERING INDEX link_line), then joins `stop` by primary key. The DISTINCT is needed because a stop has several links on a line.
- `queries/stops_within.sql`: the recursion is bounded by `near.hops < :n` with n = 1 or 2 and UNION de-duplicates, so it is a few hundred rows at worst (3 and 1 results for stop 1, under a millisecond). Safe as written.
- `stop.name` UNIQUE and `stop.id` primary key: fine for 144 stops; no evidence of duplicates or missing names.

## Not checked
- The kiosk's SQLite version (not stated); fixes were checked on 3.53.1.
- Whether the kiosk hardware is slower than this machine, and whether a `tram.db` from the nightly refresh differs from this copy.
- `PRAGMA foreign_keys` on the kiosks (no application code in the repo).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
