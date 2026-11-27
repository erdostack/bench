Decision: no-graph

The Connections panel needs no graph database, graph library or recursive query. It takes the routes at a stop, plus the routes at its partner across the road (one step), drops the school-only routes, and removes duplicates. That is two lookups and a join on the existing timetable database, and it answers in about 0.3 ms per screen, so the 20 requests a second from 1,200 screens cost under 1% of one core.

- The partner relation has a trap. The export records each pair on only one of the two stops, so the query must look for the partner in both directions. My check against a brute-force list matched on 300 of 300 random stops.
- Kai's point is right about the whole network, but the panel stops after one step. Only a panel that shows connections by changing buses would need a traversal, and that is not the rule customer services gave.
- Before it ships, check the result for a sample of stops against the customer services list by hand, and confirm how the export marks a route that is school-only on some trips but not others, since the schema has one flag per route.

The full evidence, the options considered and what would change the decision are in `docs/graph/DECISION.md` in the working directory. Nothing else in the repo was changed.
