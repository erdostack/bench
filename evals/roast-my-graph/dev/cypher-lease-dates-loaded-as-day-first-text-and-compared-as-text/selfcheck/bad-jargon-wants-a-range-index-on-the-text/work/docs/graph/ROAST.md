# Roast: leasebook graph

Temporal modelling without temporal types, range predicates without range indexes.

## Findings

### 1. expiring_leases (high)

**Problem.** Range predicate on Lease.ends has no backing range index; the predicate is non-sargable and is evaluated as a filter after expansion. Temporal properties should also be strongly typed as a matter of schema hygiene.

**Fix.** CREATE INDEX lease_ends IF NOT EXISTS FOR (l:Lease) ON (l.ends); likewise for Lease.starts. Consider adding a property type constraint.

### 2. load_leases (medium)

**Problem.** MERGE on Tenant inside the same statement as the Lease upsert widens the lock footprint.

**Fix.** Split tenants into their own load statement.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
