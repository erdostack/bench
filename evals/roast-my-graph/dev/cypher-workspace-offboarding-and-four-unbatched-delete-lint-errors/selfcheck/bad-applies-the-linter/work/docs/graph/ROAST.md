# Roast: graph/offboarding.py

## Findings

### 1. DELETE_CARDS (high)

**Problem.** Unbatched DETACH DELETE; large deletes in one transaction can exhaust memory.

**Fix.** Wrap in CALL (c) { DETACH DELETE c } IN TRANSACTIONS OF 1000 ROWS.

### 2. DELETE_WORKSPACE (high)

**Problem.** Unbatched DETACH DELETE.

**Fix.** Wrap in IN TRANSACTIONS.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
