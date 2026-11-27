# Roast: shelfnote tablet queries

store_promos is a cartesian product; pipeline it with WITH so the store is resolved first.

## Findings

### 1. store_promos (high)

**Problem.** Cartesian product anti-pattern between Store and Promo, a disconnected pattern that the planner cannot optimise.

**Fix.** Pipeline it with WITH: MATCH (s:Store {id: $store}) WITH s MATCH (p:Promo) WHERE p.active = true, and keep only active promos in the table.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
