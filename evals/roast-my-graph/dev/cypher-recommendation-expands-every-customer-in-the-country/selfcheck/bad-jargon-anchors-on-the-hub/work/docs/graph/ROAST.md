# Roast: neo4j/recs.cypher

Supernode fan-out with no index anchor. A two-for-one.

## Findings

### 1. popular_near_you (high)

**Problem.** Supernode fan-out! The anonymous (:Country) node in the middle of the pattern has no variable, which stops the planner from using the country_iso constraint as an index anchor.

**Fix.** Name the node and anchor on it: MATCH (c:Country {iso: $iso})<-[:LIVES_IN]-(peer:Customer)-[b:BOUGHT]->(p:Product) WHERE b.at >= $since ... so the query starts from the indexed Country node instead of the customer.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
