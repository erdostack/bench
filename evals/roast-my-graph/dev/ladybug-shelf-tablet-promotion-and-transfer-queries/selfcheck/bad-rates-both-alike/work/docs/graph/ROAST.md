# Roast: shelfnote tablet queries

Two cartesian products; both need rewriting before the rollout.

## Findings

### 1. store_promos (high)

**Problem.** Cartesian product of Store and Promo, slow at 2,000 stores.

**Fix.** Split it into two MATCH clauses.

### 2. transfer_distance (high)

**Problem.** Cartesian product of Store and Store.

**Fix.** Split it as well.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
