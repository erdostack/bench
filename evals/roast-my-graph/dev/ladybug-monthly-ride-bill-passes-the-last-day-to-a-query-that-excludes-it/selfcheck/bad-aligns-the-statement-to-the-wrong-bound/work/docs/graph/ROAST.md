# Roast: pedalpool billing

An off-by-one between two queries.

## Findings

### 1. account_statement (high)

**Problem.** Inconsistent date bound: <= $last_day here, < $last_day in account_totals, so the statement lists more rides than the invoice counts.

**Fix.** Change account_statement to r.ended_on < $last_day so both queries use the same half-open interval.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
