# Roast: coopmarket board reports

Reports look right.

## Findings

### 1. shop_orders (low)

**Problem.** avg of integer cents returns a float.

**Fix.** Round it in the board pack.

### 2. load_reports (low)

**Problem.** Parses the file by splitting on comments.

**Fix.** Keep the queries in Python constants.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
