# Roast: letwell model and queries

He's wrong for this model. Lease is not a join table: payments, deposits and guarantors all point
at a particular lease, and one lease is shared by up to four co-tenants. A relationship from a
tenant to a unit cannot have payments attached to it, and you would need one per co-tenant, each
with its own copy of the rent. Keep Lease as a node. I found nothing that has to change; one low
note. Details in docs/graph/ROAST.md and findings.json.

## Findings

### 1. arrears (low)

**Problem.** Rent times three is an approximation of 90 days of rent; fine for a daily worklist.

**Fix.** If it ever matters, compute the rent due from the number of rent dates in the window.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
