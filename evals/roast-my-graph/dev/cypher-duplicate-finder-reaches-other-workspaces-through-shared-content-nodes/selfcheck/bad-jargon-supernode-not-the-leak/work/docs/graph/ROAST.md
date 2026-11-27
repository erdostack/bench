# Roast: vaultshelf queries

Tenant scoping is applied consistently; the concerns are about fan-out.

## Findings

### 1. duplicates_of (high)

**Problem.** Supernode expansion: a Blob for a popular template has hundreds of thousands of HAS_CONTENT relationships and this query expands all of them before applying LIMIT.

**Fix.** Add a relationship index or cap the expansion; consider precomputing duplicate counts per Blob.

### 2. File.ws (medium)

**Problem.** Denormalised tenant discriminator duplicating the IN relationship.

**Fix.** Remove it and traverse from Workspace.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
