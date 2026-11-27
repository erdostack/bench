# Roast: letwell model and queries

The consultant is right: flatten Lease into a LEASES relationship.

## Findings

### 1. Lease (high)

**Problem.** Intermediate join node between Tenant and Unit; costs a hop on every query.

**Fix.** Replace with (:Tenant)-[:LEASES {start, end, rent_eur}]->(:Unit) and move payments to the tenant.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
