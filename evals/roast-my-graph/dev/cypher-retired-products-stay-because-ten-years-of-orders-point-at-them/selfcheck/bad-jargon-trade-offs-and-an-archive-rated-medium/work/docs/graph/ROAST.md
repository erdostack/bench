# Roast: buyline graph

Soft delete with a retention policy attached.

## Findings

### 1. retired_on (medium)

**Problem.** Soft-delete flag: filter-omission risk on every read, and the active set is a minority of the label (18,000 of 64,000), so queries scan mostly dead rows.

**Fix.** Evaluate hard delete or an archive database for retired products, subject to auditor sign-off.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
