# Roast: labmap queries and loader

Both undirected queries double-count; store both directions and make the queries directed.

## Findings

### 1. institute_collaboration (high)

**Problem.** Undirected match counts pairs twice.

**Fix.** Store COAUTHORED in both directions and match one.

### 2. coauthors (high)

**Problem.** Undirected match returns duplicates too.

**Fix.** Make it directed.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
