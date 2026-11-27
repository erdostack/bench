# Roast: neo4j/recs.cypher

Decent set of queries.

## Findings

### 1. popular_near_you (low)

**Problem.** Might be a little slow in big markets.

**Fix.** Keep an eye on it.

### 2. category_bestsellers (medium)

**Problem.** Sorts 350 products per call.

**Fix.** Add an index on units_sold.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
