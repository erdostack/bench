# Roast: labmap queries and loader

Fix the directed/undirected mismatch by storing COAUTHORED both ways.

## Findings

### 1. institute_collaboration (high)

**Problem.** Undirected traversal semantics on a directed edge store produce duplicate matches.

**Fix.** Model the relationship as bidirectional by creating the reverse COAUTHORED edge for every pair.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
