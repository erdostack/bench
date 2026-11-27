# Review: tramgraph

Both variable-length queries are dangerous.

## Findings

### 1. queries/journey.cypher (critical)

**Problem.** Matches every path of any length, then sorts to keep the shortest: will not finish on the mesh.

**Fix.** Use shortestPath((a)-[:LINK*]-(b)).

### 2. queries/nearby.cypher (high)

**Problem.** Variable-length expansion on every stop page; will explode when the network doubles.

**Fix.** Precompute neighbours.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
