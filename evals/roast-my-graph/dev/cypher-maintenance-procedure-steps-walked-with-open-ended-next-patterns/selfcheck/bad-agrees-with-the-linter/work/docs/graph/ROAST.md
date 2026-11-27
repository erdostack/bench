# Review: sopgraph

Both are unbounded variable-length patterns and must be fixed.

## Findings

### 1. steps_remaining.cypher (high)

**Problem.** Unbounded [:NEXT*] expansion can traverse the whole graph and blow up memory.

**Fix.** Store a remaining-steps count on each Step and drop the traversal.

### 2. steps_in_order.cypher (critical)

**Problem.** Unbounded [:NEXT*0..] expansion: exponential path explosion.

**Fix.** Store the step list as a property on Procedure.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
