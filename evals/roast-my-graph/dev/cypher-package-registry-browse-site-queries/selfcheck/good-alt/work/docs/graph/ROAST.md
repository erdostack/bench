# Roast: pkgatlas queries

Similar packages fans out through the license node; precompute it.

## Findings

### 1. :License / LICENSED_UNDER (high)

**Problem.** The 'Similar packages' box traverses (p)-[:LICENSED_UNDER]->(l)<-[:LICENSED_UNDER]-(other), so for popular licenses every request fans out over more than a million packages.

**Fix.** Keep the license as a filter, not a hop: precompute candidates per category offline and filter on a license property, or cache the related list per package.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
