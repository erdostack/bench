# Roast: labmap queries and loader

collaborating_pairs is doubled by the undirected match; add a.id < b.id. Nothing else.

## Findings

### 1. report.cypher collaborating_pairs (critical)

**Problem.** Each internal collaboration is counted from both ends of the undirected match, so the figure is 2x.

**Fix.** Add WHERE a.id < b.id (or count(c) / 2).

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
