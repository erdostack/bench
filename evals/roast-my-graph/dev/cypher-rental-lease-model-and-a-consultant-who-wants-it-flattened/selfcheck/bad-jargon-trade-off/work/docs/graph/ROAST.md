# Roast: letwell model and queries

It's a trade-off between expressiveness and hop count; benchmark before deciding.

## Findings

### 1. Lease (medium)

**Problem.** Reified relationship pattern. Valid, but it adds traversal depth; a LEASES relationship would be leaner.

**Fix.** Evaluate flattening Lease into a relationship and benchmark both models.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
