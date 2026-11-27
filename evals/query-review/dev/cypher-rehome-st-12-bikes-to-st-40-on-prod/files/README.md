# fleetgraph

Bikes and docking stations of the shared bicycle scheme as a Neo4j graph: where each bike is homed (the
station whose van team maintains it) and where it is docked now. The van rota, the maintenance planner and
the station map read it.

- `bin/bk prod "<cypher>"` / `bin/bk prod --file <f>`: run Cypher on the database.
- `changes/`: reviewed data changes, `NNN-<slug>.cypher`.
- `docs/`: environment, model, station closures.
