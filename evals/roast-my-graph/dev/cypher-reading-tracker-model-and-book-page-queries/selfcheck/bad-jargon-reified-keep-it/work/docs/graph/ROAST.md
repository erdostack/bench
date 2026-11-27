# Roast: shelfmates model and queries

Rating is a reified relationship, which is fine for flexibility; index Rating.stars.

## Findings

### 1. Rating (medium)

**Problem.** Reified relationship (intermediate node pattern). Gives flexibility for future features.

**Fix.** Keep Rating as a node but add an index on Rating.stars and cache loved_also_loved.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
