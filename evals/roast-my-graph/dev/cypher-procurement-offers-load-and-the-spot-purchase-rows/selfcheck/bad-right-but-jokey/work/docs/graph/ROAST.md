# Review

Good news for the board: the graph is fine, it just has commitment issues with contracts. The MERGE includes a null contract_ref and Neo4j, quite reasonably, refuses to marry a null.

## load_offers.cypher (high)

Problem: MERGE with contract_ref null for spot purchases fails, killing the file. Spot purchases: the procurement equivalent of buying snacks at the petrol station.

Fix: MERGE (s)-[r:SUPPLIES]->(p) then SET r.contract_ref = o.contract_ref.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
