# Roast: graph/offboarding.py

## Findings

### 1. DELETE_CARDS (medium)

**Problem.** Unbatched delete anti-pattern; fine at current limits but may not scale.

**Fix.** Consider CALL { } IN TRANSACTIONS for future-proofing, or keep it if atomicity matters to you.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
