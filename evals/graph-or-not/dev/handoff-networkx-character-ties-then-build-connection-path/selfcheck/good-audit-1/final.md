Added companion/connections.py. connection(conn, a, b) runs Dijkstra over the tie table with each tie's length set
to 1 / weight, the rule in docs/graph/DECISION.md, so the chain follows the strongest relationships.

An unknown id, or two characters with no chain between them, returns None; the same character at both ends returns
a one-item list.

I tried it on a small fixture of 5 characters and 6 ties, where the strong two-step route beats the weak direct tie.
