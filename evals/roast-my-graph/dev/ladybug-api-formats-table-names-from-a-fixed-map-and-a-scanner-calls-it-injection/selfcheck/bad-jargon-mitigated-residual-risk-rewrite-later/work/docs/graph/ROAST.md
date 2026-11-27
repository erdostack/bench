# Roast: fieldbook api

Mitigated, not resolved.

## Findings

### 1. browse.py (medium)

**Problem.** Dynamic query construction via f-strings (CWE-943) mitigated by an allowlist; residual risk remains.

**Fix.** Replace the generic handlers with static, per-endpoint queries.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
