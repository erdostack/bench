# Routes

- `(:Carpool)-[:DRIVES]->(:Route {routeId, retiredOn})`: `retiredOn` (DATE) is set when the carpool
  stops using the route; absent while it is in use.
- `(:Route)-[:FIRST_STOP]->(:Stop)`, then `(:Stop)-[:NEXT]->(:Stop)` to the school.
- `(:Stop {stopId, name, location, active})`.

Every route is a simple chain: the route editor gives each stop at most one `NEXT` in and one out,
never links back to an earlier stop, and never shares a stop between routes (the nightly
`route_shape_check` job fails the build if any of that is violated). Routes have 2 to 40 stops:
most neighbourhood carpools have 4 to 10, and the long rural routes that replaced the old district
bus have 25 to 40.
