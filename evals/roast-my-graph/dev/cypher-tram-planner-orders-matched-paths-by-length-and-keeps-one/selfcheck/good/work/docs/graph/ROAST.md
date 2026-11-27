# Review: tramgraph

What breaks first is the journey search, and it is already broken at today's size. journey.cypher asks Neo4j for every route of any length between two stops and only then keeps the shortest. On a network full of loops that is an astronomical number of routes; it will not finish. Use shortestPath. The nearby panel's two-stop pattern is fine.

## Findings

### 1. queries/journey.cypher (critical)

**Problem.** The pattern (a)-[:LINK*]-(b) has no upper length and ignores direction, so Neo4j has to find every route between the two stops before ORDER BY and LIMIT 1 can pick the shortest. The README says the network is a mesh with many loops and 1,800 stops; the number of routes between two stops grows exponentially with the network, so the query will not finish for ordinary pairs, and it runs on every journey search at 40 a second. Doubling the network makes it worse, not just slower.

**Fix.** MATCH (a:Stop {id: $from}), (b:Stop {id: $to}) MATCH p = shortestPath((a)-[:LINK*]-(b)) RETURN [s IN nodes(p) | s.name] AS stops, length(p) AS hops. Neo4j 5.26 also accepts MATCH p = SHORTEST 1 (a)-[:LINK]-+(b).

### 2. queries/nearby.cypher (low)

**Problem.** Variable length, but bounded at two steps and anchored on one stop by its unique id; with about three links per stop that is a few dozen rows. Fine as it is.

**Fix.** None needed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
