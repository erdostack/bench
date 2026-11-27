# Graph decision

Decision: no-graph

The Connections panel lists every non-school route that calls at a stop or at the stop across the road, which is one step from the stop to its partner and then a lookup on the membership table. Kai's whole-network view is a graph, but the panel never follows a route from one stop to a second route, so no traversal runs. A query of this shape costs about 0.3 ms on SQLite at the stated scale, so the 20 calls a second from the screens need nothing more than plain joins.

## Workload facts

- Stops: about 6,900 (stated by the user)
- Routes: 380 (stated by the user)
- Stop-route rows: 41,000 (stated by the user)
- Rebuild: nightly from the scheduling system, so the data is static during the day (stated by the user; `README.md`)
- Load: about 1,200 screens refreshing once a minute, which is 1,200 / 60 = 20 panel queries a second (stated by the user, with the arithmetic derived here)
- Rule, as customer services state it: every route you can catch at this stop or at the stop across the road, and leave out the school-only routes (stated by the user)
- Partner relation: `stop.paired_stop_id` gives the stop on the other side of the road; the export records each pair once, on one of the two stops only (`db/schema.sql`, lines 7 to 9). So the partner of a stop is either its own `paired_stop_id` or a stop whose `paired_stop_id` names it, and a one-directional lookup misses half of the pairs.
- Membership: `stop_route (stop_id, route_id)` with that as primary key, so lookups by stop are served by the key (`db/schema.sql`, lines 19 to 23)
- School-only flag: `route.school_only`, one flag per route (`db/schema.sql`, lines 12 to 16)
- Existing query: `sql/routes_here.sql` is the top-line query for routes at one stop; there is no `sql/connections.sql` yet (`sql/routes_here.sql`, `boards/board.py` line 17)
- Index gap: no index on `stop.paired_stop_id` (`db/schema.sql`); the reverse partner lookup therefore scans the stop table, which is 6,900 rows
- Measured, synthetic on SQLite 3.53.1 (generator in scratch, not the real timetable; 6,900 stops, 1,500 pairs recorded once, 380 routes with 20% school-only, 41,000 stop-route rows; the union of both partner directions, one hop, and the school-only filter): the query matched a brute-force check for 300 of 300 random stops (measured)
- Measured: 0.337 ms per panel query on average, with 6.8 routes per panel on average in the synthetic data (measured)
- Derived: 20 queries a second x 0.337 ms = 6.7 ms of database time per second, under 1% of one core (derived from the measurement above)
- Plan (measured with `EXPLAIN QUERY PLAN`): the stop's own routes come from the `stop_route` key; the partner lookup scans `stop`; the route filter is by primary key on `route` (measured)
- unknown: whether the pairs form a matching (a stop in more than one pair) — the schema does not enforce it, and the query handles several partners either way; the real number of pairs; whether a route can be school-only on some trips and not others — the schema has one flag per route; whether a route that only drops passengers at a stop should appear as a route you can catch there (the schema does not say); the real distribution of routes per stop

## Options considered

- graph-database (a dedicated graph store, Kai's proposal): rejected, because the panel reads one step to the partner stop and then one lookup on the membership table, and a nightly rebuild would have to feed a second store for a query that takes 0.3 ms in SQLite
- in-process-library (the timetable loaded into memory with a graph library): rejected, because no traversal needs a loaded graph; the panel is a join across one link table with a one-step partner lookup, and the existing SQLite file answers it in well under a millisecond
- recursive-sql (recursive queries on the timetable database already run): rejected, because the rule stops at one step; a recursive query would be needed only if the panel were to show transfers, which is not in the stated rule
- no-graph (plain joins, with one step to the partner stop): chosen, because every query is a lookup plus joins that cross the membership table at most once, the partner relation is followed for one step only, and no whole-network algorithm runs

## What would change the decision

- A change to the panel so that it shows routes reached by a change of bus (two or more routes from a stop, or a fixed second hop through another stop) would move this to recursive-sql, written as self-joins for a fixed depth; the customer services rule would have to say so
- A change to show journeys across the whole network, with unbounded transfers, would move this to in-process-library if the timetable fits in memory and the nightly rebuild meets the freshness the operator sets, and to graph-database only if it became an online service that SQL measured failing at that depth (the operator and customer services set those limits, not the repo)
- A measured panel time over the budget the screens' owner sets, on the real database, would first call for an index on `stop.paired_stop_id` or a cached partner table rebuilt each night, which is a remedy inside no-graph and not a change of option
- Trial before shipping: run the connections query on a copy of the real nightly export for about 200 stops, including stops on both sides of several pairs and a stop with school-only routes, and check the result against the customer services list by hand
