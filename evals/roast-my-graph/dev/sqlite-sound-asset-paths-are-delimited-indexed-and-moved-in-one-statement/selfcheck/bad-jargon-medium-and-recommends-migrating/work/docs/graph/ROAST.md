# Roast: parks register

## Findings

### 1. asset.path (medium)

**Problem.** Materialized path pattern: denormalised hierarchy with update anomalies; GLOB predicates are not sargable.

**Fix.** Migrate to an adjacency list with a closure table.

### 2. children (low)

**Problem.** Temp B-tree for ORDER BY.

**Fix.** Add an index on (depth, name).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
