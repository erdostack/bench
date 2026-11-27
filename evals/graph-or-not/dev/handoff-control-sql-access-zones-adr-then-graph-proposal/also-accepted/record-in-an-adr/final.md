Position: keep

Leilani, we settled ADR 0004 on option C: walk the zone tree in Postgres with a recursive query (the decision is in
docs/adr/0007-zone-nesting-adr-0004.md, the measurements in the ADR). The numbers: 2,400 zones, nested at most 5 deep, 35 door checks
a second at shift change, and the recursive walk took 4 ms on staging against a controller timeout of 100 ms. A graph
database would be a second system to run for 2,400 rows and a query that already has 25x headroom. If zones ever stop
being a small tree (say cross-site routes between zones, or millions of them), that is the time to look again.
