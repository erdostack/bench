# Roast: merge_customers.cypher

## Findings

### 1. move_referrals (high)

**Problem.** Merging duplicates that referred each other creates a self-loop REFERRED on keep.

**Fix.** Delete the link between keep and dup first.

### 2. move_orders (medium)

**Problem.** CREATE could duplicate PLACED.

**Fix.** Use MERGE.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
