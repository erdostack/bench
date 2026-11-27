# Review: tramgraph

journey.cypher has an unbounded variable-length pattern; add an upper bound.

## Findings

### 1. queries/journey.cypher (high)

**Problem.** Unbounded variable-length relationship pattern (an anti-pattern flagged by every Cypher linter).

**Fix.** Bound it: [:LINK*..40], which is more than any journey needs.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
