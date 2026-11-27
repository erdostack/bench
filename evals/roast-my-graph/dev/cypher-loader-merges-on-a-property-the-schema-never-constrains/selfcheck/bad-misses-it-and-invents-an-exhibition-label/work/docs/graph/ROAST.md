# Roast: galleria graph

A tidy little graph with one gap.

## Findings

### 1. Exhibition (high)

**Problem.** Exhibition nodes have no constraint on their id.

**Fix.** Add a uniqueness constraint on Exhibition.id.

### 2. maker_search (low)

**Problem.** Prefix search could use a full-text index.

**Fix.** Add one if search grows.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
