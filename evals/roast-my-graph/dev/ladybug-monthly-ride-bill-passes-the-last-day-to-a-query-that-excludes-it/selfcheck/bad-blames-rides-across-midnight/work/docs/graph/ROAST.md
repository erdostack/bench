# Roast: pedalpool billing

Nothing wrong in the billing queries.

## Findings

### 1. Ride.started_on (low)

**Problem.** Rides spanning midnight at month end appear in the month they end, which can surprise customers.

**Fix.** Explain the rule on the statement.

### 2. Employs (low)

**Problem.** Unused by billing.

**Fix.** Remove it or document it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
