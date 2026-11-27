# Roast: vinylgraph catalogue loader

Your teammate is right; the one-statement MERGE is simpler and cannot skip rows.

## Findings

### 1. link_artists (high)

**Problem.** MATCH silently drops rows when a node is missing, so credits can be lost.

**Fix.** Replace the four statements with one MERGE of the whole pattern, as in the PR.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
