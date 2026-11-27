# sopgraph

Maintenance procedures (SOPs) for the depot technicians' tablets, stored in Neo4j 5.26.

Model:

    (:Procedure {id, version, title})-[:FIRST]->(:Step {uid, n, text})-[:NEXT]->(:Step)-[:NEXT]->...

A procedure version is an ordered list of steps. Versions are immutable: a change publishes a new version with its
own, new step nodes. `loader/load.py` is the only thing that writes to the database (the tablets connect with a
read-only user); it builds each version's chain from the YAML file's step list, in order.

Limits enforced by the loader: at most 40 steps per procedure.

Queries the tablet app runs are in `queries/`.
