# Roast: vaultshelf queries

Multi-tenancy by convention is multi-tenancy by hope.

## Findings

### 1. duplicates_of (high)

**Problem.** Tenant isolation here, as in the other queries, depends on a predicate the developer must remember to write. Query-level tenancy predicates are a weak isolation pattern with no defence in depth.

**Fix.** Adopt a per-tenant label or separate databases, and enforce isolation with role-based access control instead of predicates.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
