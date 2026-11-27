# Roast: pagerline team page queries

The handover statement builds a cartesian product; split it. The cards look fine.

## Findings

### 1. hand_over_shift (high)

**Problem.** Cartesian product between from and to: Neo4j warns about this and it can blow up memory.

**Fix.** Split into two MATCH clauses.

### 2. open_incidents (medium)

**Problem.** Filters closed_at after the expansion.

**Fix.** Add an index on closed_at.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
