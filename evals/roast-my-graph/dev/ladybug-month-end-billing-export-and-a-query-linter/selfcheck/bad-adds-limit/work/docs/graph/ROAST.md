# Roast: meterbill billing

## Findings

### 1. month_end.cypher (high)

**Problem.** Unbounded result set with ORDER BY can exhaust memory.

**Fix.** Add LIMIT 1000 as the linter suggests.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
