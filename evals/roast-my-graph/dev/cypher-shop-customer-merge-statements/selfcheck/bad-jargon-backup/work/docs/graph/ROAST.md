# Roast: merge_customers.cypher

## Findings

### 1. drop_duplicate (high)

**Problem.** DETACH DELETE is a destructive cascading anti-pattern.

**Fix.** Take a backup before each merge and ask support to confirm the customer id twice.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
