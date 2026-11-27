# Route report: where the routing runs

Decision: in-process-library

## Workload facts (from the owner)

- Production mesh: about 2,300 relays and 14,000 one-way links; the controller republishes the GraphML every 5
  minutes; on-call runs the report about 40 times a day.
- Firmware: a message is dropped after 6 hops, so a route may use at most 6 links. A relay reachable only in
  more hops is unreachable, and the report shows it as such (inf).
- docs/routing.md: cost in ms (the file stores latency_us), source 0, no route inf.

## Options considered

- graph-database (network team): rejected; a reimport every 5 minutes for a millisecond computation.
- in-process-library: chosen; NetworkX already loads the file (relay/topology.py).
- recursive-sql: there is no SQL database here.
- no-graph: no, it is a weighted path search.

## What would change the decision

- Route queries from the relays themselves at high rates, or a topology too big for the ops box.
