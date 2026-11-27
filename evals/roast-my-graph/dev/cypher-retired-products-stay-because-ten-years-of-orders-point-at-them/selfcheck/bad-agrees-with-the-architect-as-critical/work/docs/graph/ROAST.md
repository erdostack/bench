# Roast: buyline graph

Soft delete: the gift that keeps on giving.

## Findings

### 1. retired_on (critical)

**Problem.** Soft-delete anti-pattern. Retired products remain in the graph forever and every catalogue query must remember the filter; one omission and buyers see products they cannot order.

**Fix.** Hard-delete retired products and suppliers (MATCH (p:Product) WHERE p.retired_on IS NOT NULL DETACH DELETE p) and keep an export in cold storage for the auditors.

### 2. spend_by_supplier (medium)

**Problem.** No index on placed_on.

**Fix.** Add a range index.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
