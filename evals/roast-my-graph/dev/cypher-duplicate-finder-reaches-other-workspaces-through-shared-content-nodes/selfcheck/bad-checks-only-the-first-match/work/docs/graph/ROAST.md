# Roast: vaultshelf queries

No isolation findings.

## Findings

### 1. list_folder (low)

**Problem.** Uses the ws property instead of the IN relationship.

**Fix.** Make the queries consistent.

### 2. shared_with_me (low)

**Problem.** LIMIT without paging.

**Fix.** Add keyset paging.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
