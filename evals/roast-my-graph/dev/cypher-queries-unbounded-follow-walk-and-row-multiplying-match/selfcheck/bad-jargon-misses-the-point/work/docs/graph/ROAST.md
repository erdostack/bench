# Roast: queries/feed.cypher

Unbounded variable-length paths! Cartesian products! Eager operators! This file is an anti-pattern bingo card.

## Findings

### 1. follower_reach (critical)

**Problem.** Unbounded variable-length path anti-pattern! The direction of the arrow is also suspicious and count(DISTINCT) is an eager aggregation.

**Fix.** Flip the arrow so it reads (me)-[:FOLLOWS*]->(fan) and use count(*) instead of count(DISTINCT fan) to avoid the eager operator.

### 2. listener_stats (high)

**Problem.** Cartesian product alert: the planner will warn about this query. Also, the Genre lookup has no index anchor.

**Fix.** Add a range index on Genre.slug and a USING INDEX hint so the second MATCH is anchored; the Cartesian product warning can then be ignored.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
