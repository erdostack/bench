# Roast: meterbill billing

## Findings

### 1. month_end.cypher (medium)

**Problem.** Unbounded-result anti-pattern; ORDER BY forces a full sort.

**Fix.** Consider SKIP/LIMIT pagination or a smaller LIMIT, depending on how much memory the host has.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
