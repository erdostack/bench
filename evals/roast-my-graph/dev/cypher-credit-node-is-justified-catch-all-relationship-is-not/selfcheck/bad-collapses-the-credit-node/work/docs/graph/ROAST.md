# Roast: reelbase model

Nineteen million join rows in a trench coat.

## Findings

### 1. Credit (critical)

**Problem.** Join table kept as a node: Credit only exists to connect a Person to a Production, turning every filmography lookup into a two-hop traversal across 19 million pointless nodes.

**Fix.** Replace Credit with a direct relationship (p:Person)-[:CREDITED_ON {role, billing_order}]->(prod:Production) and delete the Credit label.

### 2. (:Person)-[:HOLDS]->(:Credit) (high)

**Problem.** HOLDS and ON are plumbing for the join node.

**Fix.** Remove both once Credit is a relationship.

### 3. RELATED (medium)

**Problem.** Generic relationship type with a kind property.

**Fix.** Split into specific relationship types such as SPOUSE_OF, REPRESENTED_BY and COLLABORATES_WITH.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
