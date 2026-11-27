# Roast: transit db (db/, app/, transit.db)

Verdict: Yes, something is badly wrong: the stop page shows routes that do not call at the stop. `routes_at_stop.sql` matches the stop id as a substring of a comma-separated string, so on the shipped data 999 of the 4,800 stops list wrong routes (stop 7 lists 309 of 310 routes; one actually calls there). Store the stops of a route as rows, not as one string.

Judged against:
- SQLite; version not stated in the repo. Run on the shipped copy with SQLite 3.53.1 (python `sqlite3`), read-only (README.md, transit.db).
- 4,800 stops (ids 1 to 4800), 310 routes; the file is rebuilt from the scheduling system every night (README.md). Shipped data: 11,187 stop calls, 36 per route on average, 55 at most, no repeats within a route, no ids missing from `stop`.
- The stop page lists the routes that call at the stop; the planner finds one-change journeys (README.md). Rates and latency targets: not stated.

## Findings

### critical: `routes_at_stop.sql`
The stop page asks "which routes call here?" and the database answers "any route whose string contains the digits". Stop 7 is, apparently, served by everything with a 7 in it.
Problem: `WHERE stop_sequence LIKE '%' || :stop_id || '%'` matches the id as a substring, so stop 17 also matches routes that call at 117, 170, 2175 and so on. Run on transit.db, 999 of 4,800 stops return wrong routes, 35,245 extra route rows in all; stop 7 returns 309 routes and one serves it, stop 17 returns 240 and four serve it. `stop_page` in app/planner.py returns this result as is, to the user, with no check. `routes_at` uses the same file and only gets correct answers because `one_change` re-checks every route (see below).
Fix: read the rows once `route_stop` exists (see `stop_sequence`): `SELECT r.id, r.short_name, r.mode FROM route r JOIN route_stop rs ON rs.route_id = r.id WHERE rs.stop_id = :stop_id ORDER BY r.short_name;`. On a copy of transit.db this returns 1 route for stop 7, using a covering index search. Stopgap only, if the migration has to wait: match whole items, `WHERE ',' || stop_sequence || ',' LIKE '%,' || :stop_id || ',%'`; it is exact on this data but still scans all 310 routes and leaves the text as the only record.

### critical: `stop_sequence`
Problem: `route.stop_sequence` is the only record of which stops a route serves, stored as one comma-separated string. Two statements read it and one is wrong on the shipped data (`routes_at_stop.sql` above); the other, `stops_of_route.sql`, returns the whole string for `stops_of` to split and convert in Python, and `one_change` calls it once per candidate route. Nothing checks that an id in the string is a real `stop`, the lookup by stop cannot use an index, and every statement has to get the text matching right again. Rated as the worst damage it causes.
Fix: one row per stop call, with keys to both sides and the index for the direction the stop page reads (assumes SQLite 3.35 or later for `DROP COLUMN`; verified on 3.53.1):
`CREATE TABLE route_stop (route_id INTEGER NOT NULL REFERENCES route (id), seq INTEGER NOT NULL, stop_id INTEGER NOT NULL REFERENCES stop (id), PRIMARY KEY (route_id, seq)) WITHOUT ROWID;` and `CREATE INDEX route_stop_by_stop ON route_stop (stop_id, route_id);`
Migration, split with a recursive query (on a copy it produced 11,187 rows, equal to the number of ids in the strings):
`WITH RECURSIVE s(route_id, n, stop_id, rest) AS (SELECT id, 0, NULL, stop_sequence || ',' FROM route UNION ALL SELECT route_id, n + 1, CAST(substr(rest, 1, instr(rest, ',') - 1) AS INTEGER), substr(rest, instr(rest, ',') + 1) FROM s WHERE rest <> '') INSERT INTO route_stop SELECT route_id, n, stop_id FROM s WHERE stop_id IS NOT NULL;`
Then `ALTER TABLE route DROP COLUMN stop_sequence;`, change `stops_of_route.sql` to `SELECT stop_id FROM route_stop WHERE route_id = :route_id ORDER BY seq;`, drop the string parsing in `stops_of`, and make the nightly rebuild (not in this repo) write `route_stop` instead of the string. Keeping the string as the source of truth, or adding an index over it, is not the fix. Foreign keys only hold if the application runs `PRAGMA foreign_keys = ON` on each connection; `app/planner.py` does not.

### low: `one_change`
Problem: It is correct on the shipped data, only because it re-checks what the SQL gets wrong (`origin not in s1` skips false routes at the origin; `destination in s2` empties `before_dest` for false routes at the destination). The cost is a `stops_of` query and a string split per candidate route, inside a loop over `routes_at(destination)`, and the false candidates make the loops bigger: stop 7 starts from 309 routes. Measured in memory on a copy: 3 to 16 ms per query, so this is tidiness, not a problem at 310 routes.
Fix: After the `route_stop` migration, do the search in SQL: `SELECT a.route_id, a.stop_id, b.route_id FROM route_stop o JOIN route_stop a ON a.route_id = o.route_id AND a.seq > o.seq JOIN route_stop b ON b.stop_id = a.stop_id AND b.route_id <> a.route_id JOIN route_stop d ON d.route_id = b.route_id AND d.seq > b.seq WHERE o.stop_id = :origin AND d.stop_id = :destination;` It gave the same route pairs as `one_change` for the three origin and destination pairs tried (7 to 17, 1 to 2, 4184 to 3173) and returns every valid change stop, not only the first one `one_change` keeps; take the smallest `a.seq` per route pair if only the first matters.

## Holds up
- `headway`: composite key `(route_id, day_type)` serves lookups by route, which is how it would be read; the `CHECK` on `day_type` and the key stop duplicates. Every route has headway rows and none are orphaned in the shipped data. Nothing reads it in the files; that is not a defect.
- `route`: `short_name` is `UNIQUE` and `mode` is checked; `stops_of_route.sql` itself searches by primary key (`SEARCH route USING INTEGER PRIMARY KEY`). Its only problem is the string it returns, filed under `stop_sequence`.
- `stop`: `id` is the primary key, which is the lookup key; `lat` and `lon` are not used by any file here.

## Not checked
- The nightly rebuild from the scheduling system is not in the repo, so the load path, who else reads `route` and whether `stop_sequence` has other consumers could not be checked; the migration must be reconciled with it.
- Request rates, latency targets and the planner's real call volume are not stated; planner timings are from an in-memory copy of transit.db on this machine, not production.
- The route-pair comparison of the SQL replacement for `one_change` covers three pairs, not every pair.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
