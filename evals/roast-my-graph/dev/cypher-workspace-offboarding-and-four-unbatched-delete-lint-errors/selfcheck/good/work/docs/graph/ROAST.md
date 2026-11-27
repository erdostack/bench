# Roast: graph/offboarding.py

## Findings

### 1. lint/report.txt (low)

**Problem.** The four UNBATCHED_DELETE errors are false alarms for this file and will keep failing CI.

**Fix.** Suppress UNBATCHED_DELETE for graph/offboarding.py with a comment that names api/limits.py as the bound and the README's all-or-nothing rule as the reason.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
