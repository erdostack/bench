# Roast: coopmarket board reports

Fan-out, meet sum.

## Findings

### 1. region_revenue (high)

**Problem.** Row multiplication: the Contains fan-out duplicates order rows before aggregation.

**Fix.** Change sum(o.total_cents) to sum(DISTINCT o.total_cents).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
