# Roast: orgline graph

Four queries swimming against the current.

## Findings

### 1. approver_for (high)

**Problem.** Directional mismatch: the traversal runs against the stored direction of REPORTS_TO, an inverted-traversal smell.

**Fix.** Reverse the pattern to (e)<-[:REPORTS_TO*1..9]-(boss). Do the same in chain_of_command, direct_reports and headcount_under, and update docs/model.md to document REPORTS_TO as manager to report.

### 2. managment_level (low)

**Problem.** Typo in a property name.

**Fix.** Rename.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
