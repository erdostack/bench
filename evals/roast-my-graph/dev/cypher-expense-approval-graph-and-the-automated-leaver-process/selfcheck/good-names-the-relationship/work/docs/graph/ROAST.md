# Roast: approvals-graph

## Findings

### 1. APPROVED (high)

**Problem.** remove_leaver detach-deletes the employee, so their APPROVED relationships (and SUBMITTED, AWAITS) go too; approvals are no longer attributable and pending claims are orphaned.

**Fix.** Soft-retire the Employee (left_on property) instead of deleting; hand AWAITS over to the manager first.

### 2. cost_center (low)

**Problem.** Alias spelled differently from the CostCentre label.

**Fix.** Rename to cost_centre.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
