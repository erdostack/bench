# Roast: leasebook graph

Mostly fine.

## Findings

### 1. rent_roll_on (medium)

**Problem.** Scans all Lease nodes each time it runs.

**Fix.** Start from buildings and expand, or add an index.

### 2. Tenant (low)

**Problem.** Tenants are created implicitly by the lease load and never get a name.

**Fix.** Load tenants from their own export.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
