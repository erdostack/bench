# Roast: transit-db schema, queries and planner

Verdict: Not sound. The stop page lists routes that do not call at the stop, and the cause is the packed stop_sequence column, which every route lookup matches as text. On the shipped copy, 35,245 of 46,432 rows the stop page returns are wrong. The fix is a route_stop table; the planner's answers were right in every case checked, and its cost is secondary.

Judged against:
- SQLite, version not stated in the repo; transit.db was last written by SQLite 3.53.1, README.md and the file header
- 4,800 stops (ids 1 to 4800) and 310 routes, README.md
- Rebuilt every night from the scheduling system, README.md
- The stop page lists the routes that call at the stop, README.md
- The planner finds one-change journeys through a shared stop, README.md
- stop_sequence holds stop ids in travel order, comma-separated, db/schema.sql
- Request rates for the stop page and the planner are not stated

## Findings

### critical: `stop_sequence`
Every route lookup treats this column as a sentence, and a sentence containing "1" is a sentence containing "1".
Problem: route.stop_sequence packs each route's stops into one comma-separated text value, and both routes_at_stop.sql and planner.py match and parse it as text. On the shipped copy, 35,245 of the 46,432 (stop, route) rows the stop page returns for stops 1 to 4800 name a route that does not call at that stop. Stop 1's page lists all 310 routes, and only 2 call there. Nothing can check that the listed stop ids exist, and a LIKE match finds ids inside longer ids.
Fix: Replace the column with a route_stop table: route_id, seq, stop_id, PRIMARY KEY (route_id, seq), and `CREATE INDEX route_stop_by_stop ON route_stop (stop_id, route_id)`. Migrate with `INSERT INTO route_stop (route_id, seq, stop_id) SELECT r.id, j.key + 1, CAST(j.value AS INTEGER) FROM route r, json_each('[' || r.stop_sequence || ']') j;`, then drop stop_sequence. Verified in memory on SQLite 3.53.1 against the copy: 11,187 rows migrated, and the join returns the exact route list for all 4,800 stops. Put the migration in the nightly rebuild, since that rebuilds the file.

### critical: `routes_at_stop.sql`
The stop page matches a number inside a longer number. Stop 1 is a hard case to explain to a bus rider.
Problem: The stop page runs `stop_sequence LIKE '%' || :stop_id || '%'`, so a stop id matches inside longer ids. On the shipped copy this gives wrong rows for 999 of the 4,800 stops, and 35,245 of 46,432 returned rows are wrong. The stop page is customer-facing and the README says it lists the routes that call at the stop.
Fix: Stopgap only: `WHERE ',' || stop_sequence || ',' LIKE '%,' || :stop_id || ',%'`. On the copy this returns the exact list for all 4,800 stops, but the packed text stays the only record of the relationship. The structural fix is the route_stop table under stop_sequence, and this statement then becomes a join on route_stop.stop_id.

### medium: `one_change`
The planner always gets the right answer by checking its own work, and it pays for that check in queries.
Problem: one_change calls stops_of inside the loop over destination routes, once for every origin route and destination route pair. Its candidate lists come from the same LIKE match, so for origin stop 1 it makes 928 text-parsing queries per search, against 2 routes that really call there. The journeys it returned were correct in all 60 random pairs checked, because its own origin and destination guards drop the false matches. The cost is in the search, not the answer.
Fix: After the route_stop migration, get the candidate routes with a join on stop_id, and fetch each route's stops once before the origin loop instead of inside it. The after_origin and before_dest walk can stay as it is.

### low: `headway`
A table nobody in the repo reads is either somebody else's problem or a very well-kept secret.
Problem: No file in the repo reads headway, so the table is either read by something outside this repo or stored for nothing. This is a question to confirm. Nothing in the copy is broken: PRAGMA foreign_key_check returns no rows.
Fix: Confirm what reads headway. If nothing does, drop it in the migration. If it stays, confirm that the nightly build turns foreign_keys on, since SQLite leaves it off on a new connection.

## Holds up
- `stops_of_route.sql`: looks up one route by its primary key, so it is an index search. It would change if the lookup moved to a column with no index.
- `headway`: its primary key (route_id, day_type) leads with route_id, so lookups by route are served. The CHECK constraints on day_type are correct for the data.
- `route.mode`: the CHECK list matches the three modes in the copy (bus, tram, ferry).
- The planner's shared-stop walk: the after_origin and before_dest logic gave the same journeys as an exact reference for 60 random origin and destination pairs. Its two guards (origin in the first route, destination in the second) remove the false matches. This depends on those guards staying in place.
- The route scan in routes_at_stop.sql: the plan is a scan of 310 routes, which is fine at this size. It would change at a route count far above 310.

## Not checked
- The nightly rebuild script is not in the repo, so the migration cannot be put in it or confirmed there.
- The stored text was checked for missing stop ids (none on the copy) and repeated stops within a route (none on the copy). Loops and bad ids cannot be ruled out for the live feed.
- The planner was compared on 60 random pairs and four hand-picked pairs, not all 4,800 by 4,800.
- Request rates for the stop page and the planner are not stated, so the medium rating for one_change assumes nothing about how often it runs.
- The stopgap and the migration were verified in memory on SQLite 3.53.1 against a read-only copy. transit.db itself was not changed, and no timings were taken on a server.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
