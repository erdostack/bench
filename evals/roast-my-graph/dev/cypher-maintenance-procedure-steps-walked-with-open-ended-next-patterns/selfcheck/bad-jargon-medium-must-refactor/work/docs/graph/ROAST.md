# Review: sopgraph

Unbounded var-length traversal is a known Cypher anti-pattern; medium, refactor both.

## Findings

### 1. steps_in_order.cypher (medium)

**Problem.** Unbounded variable-length path anti-pattern; risk of path explosion as data grows.

**Fix.** Refactor to MATCH (p)-[:HAS_STEP]->(s) with a HAS_STEP relationship per step and drop NEXT.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
