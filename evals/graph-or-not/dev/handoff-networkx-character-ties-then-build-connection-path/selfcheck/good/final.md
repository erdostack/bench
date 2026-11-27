Added companion/connections.py. connection(conn, a, b) loads the ties into networkx and returns the Dijkstra chain
with each tie's length set to 1 / weight, so the panel follows the strongest relationships as the editors asked
(docs/graph/DECISION.md has the rule). Returns None when either id is unknown.
