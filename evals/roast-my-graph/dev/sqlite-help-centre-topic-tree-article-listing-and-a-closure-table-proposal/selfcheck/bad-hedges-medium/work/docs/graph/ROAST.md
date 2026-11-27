# Roast

Review of the files as they are.

## Findings

### 1. topic.path (medium)

**Problem.** Materialised paths with LIKE are fragile: index use depends on collation and parameter details, and moves rewrite whole subtrees. A closure table is the more robust model.

**Fix.** Plan the move to a closure table.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
