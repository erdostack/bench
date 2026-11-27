# Roast: meterbill billing

## Findings

### 1. billing/export.py (low)

**Problem.** The completeness checks (meters_without_reading, meters_without_owner, row count) are manual runbook steps; a skipped step would go unnoticed.

**Fix.** Run the two check queries and the row-count comparison inside export.py and refuse to write the file if they fail.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
