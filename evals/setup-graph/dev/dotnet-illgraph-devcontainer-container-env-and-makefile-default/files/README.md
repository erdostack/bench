# illgraph

Interlibrary loans for the county's eleven branch libraries: which branch sends what to whom, and how a
request hops when the nearest holding branch has no copy on the shelf.

    (:Branch)-[:SENDS_TO {days}]->(:Branch)
    (:Request)-[:ROUTED_VIA {step}]->(:Branch)

## The graph

Neo4j 5.26.24 (GRAPH_TAG in the Makefile), Community edition. Work in the dev container: it starts the
graph for you with `make graph-up`. Then:

    make seed                     # create the constraints
    make q F=queries/slow_routes.cypher

The query tool is a small .NET 8 console app in src/IllGraph.Query. Connection settings come from
graph.env (not for sharing outside the team).
