# Roast: pagerline team page queries

team_health has a cartesian product that inflates members; use count(DISTINCT p).

## Findings

### 1. team_health (high)

**Problem.** Cartesian product anti-pattern: disconnected patterns multiply rows and inflate the members count.

**Fix.** Use count(DISTINCT p) AS members and keep the rest.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
