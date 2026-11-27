# Roast: reelhouse home and title queries

watch_next has a cartesian product producing duplicates; add DISTINCT.

## Findings

### 1. watch_next (high)

**Problem.** Cartesian product: disconnected patterns cause row explosion and duplicate titles.

**Fix.** Add RETURN DISTINCT and lower the LIMIT to 10 to cut the duplicates.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
