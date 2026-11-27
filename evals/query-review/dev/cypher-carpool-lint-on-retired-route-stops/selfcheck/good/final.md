The linter is wrong for this data, and its suggested `*0..10` would break the change.

docs/routes.md: every route is a simple chain (one NEXT in and out per stop, no loops back, no shared stops, checked every night by `route_shape_check`), and routes have up to 40 stops; the long rural ones have 25 to 40. So `[:NEXT*0..]` from a route's first stop can only walk that route's chain, at most 39 hops: it can't fan out or loop. Capping it at 10 would leave stops 12-40 of the rural routes active on the drivers' map.

I left 0029 as it is. To make CI green, suppress CL031 for this file (or, if you prefer an explicit cap, `*0..39` is the tightest correct bound). To check on staging: `MATCH (r:Route)-[:FIRST_STOP]->(:Stop)-[:NEXT*0..]->(s:Stop) WHERE r.retiredOn IS NOT NULL RETURN count(s)` and `PROFILE` it to see the expansion stays per route.
