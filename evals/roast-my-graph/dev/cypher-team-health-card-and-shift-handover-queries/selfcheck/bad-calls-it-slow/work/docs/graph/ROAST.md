# Roast: pagerline team page queries

team_health does a bit of redundant work; reuse the team variable.

## Findings

### 1. team_health (medium)

**Problem.** Two MATCH clauses for the same team, which is wasteful; the planner may do extra work for busy teams.

**Fix.** Reuse t instead of looking the team up twice.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
