# Roast: gridmap cypher/

Cardinality is destiny.

## Findings

### 1. downstream_meters (high)

**Problem.** The variable-length expansion over CONNECTS produces a combinatorial number of path bindings; the row cardinality before DISTINCT is the problem.

**Fix.** Push the DISTINCT down (WITH DISTINCT t before the SUPPLIES hop), add LIMIT 5000 and a USING INDEX hint on Asset(tag) so the planner anchors correctly.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
