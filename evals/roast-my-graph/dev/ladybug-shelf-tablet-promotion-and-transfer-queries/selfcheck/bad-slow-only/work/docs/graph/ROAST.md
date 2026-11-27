# Roast: shelfnote tablet queries

store_promos does a bit too much scanning; cache it.

## Findings

### 1. store_promos (medium)

**Problem.** Scans the whole Promo table on every refresh; wasteful at 700 promotions.

**Fix.** Add a filter on active first or cache the result for five minutes.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
