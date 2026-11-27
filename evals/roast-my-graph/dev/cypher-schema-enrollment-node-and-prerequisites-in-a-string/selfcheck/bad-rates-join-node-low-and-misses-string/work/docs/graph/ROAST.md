# Roast: coursegraph

Mostly fine. A couple of nits.

## Findings

### 1. Enrollment (low)

**Problem.** Enrollment could arguably be a relationship rather than a node, but it works.

**Fix.** Consider revisiting if the model is ever refactored.

### 2. classmates (high)

**Problem.** No LIMIT pushdown before the aggregation.

**Fix.** Aggregate in a subquery.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
