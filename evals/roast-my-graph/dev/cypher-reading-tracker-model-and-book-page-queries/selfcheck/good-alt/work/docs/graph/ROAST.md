# Roast: shelfmates model and queries

Collapse the Rating node into a RATED relationship; it only adds a hop.

## Findings

### 1. (:Reader)-[:GAVE]->(:Rating)-[:OF]->(:Book) (high)

**Problem.** An in-between node with no other connections; doubles the hops on the hot book-page traversals.

**Fix.** Collapse into one relationship Reader-[:RATED {stars, rated_at}]->Book and migrate the 18M ratings.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
