# Roast: orgline graph

It is hard to trust an approval chain that cannot spell management.

## Findings

### 1. managment_level (high)

**Problem.** The approval logic depends on a misspelt property. Any correctly spelt write would silently create a second property and approvals would break.

**Fix.** Rename to management_level everywhere immediately.

### 2. tmp_idx_2 (high)

**Problem.** A temporary index in production schema.

**Fix.** Drop and recreate with a proper name.

### 3. chain_of_command (medium)

**Problem.** Variable-length traversal up to 9 hops.

**Fix.** Lower the bound.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
