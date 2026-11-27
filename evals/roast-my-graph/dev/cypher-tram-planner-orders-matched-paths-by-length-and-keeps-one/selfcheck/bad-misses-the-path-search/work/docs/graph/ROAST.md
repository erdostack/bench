# Review: tramgraph

The schema is in good shape: unique constraint on Stop id, indexes on names. A few notes.

## Findings

### 1. schema/load.cypher (medium)

**Problem.** The stop rows MERGE on id and then SET the name, so a renamed stop silently keeps one node; fine, but log renames.

**Fix.** Record the previous name.

### 2. line_stops.cypher (low)

**Problem.** Sorts by seq without a tiebreak.

**Fix.** Add id.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
