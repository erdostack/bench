// Run in order with $keep and $dup, in one transaction, by tools/merge.py.

// name: move_orders
MATCH (keep:Customer {id: $keep}), (dup:Customer {id: $dup})
MATCH (dup)-[r:PLACED]->(o:Order)
CREATE (keep)-[:PLACED]->(o)
DELETE r;

// name: move_addresses
MATCH (keep:Customer {id: $keep}), (dup:Customer {id: $dup})
MATCH (dup)-[r:LIVES_AT]->(a:Address)
MERGE (keep)-[n:LIVES_AT]->(a)
  ON CREATE SET n.primary = false
DELETE r;

// name: move_referrals
MATCH (keep:Customer {id: $keep}), (dup:Customer {id: $dup})
OPTIONAL MATCH (dup)-[out:REFERRED]->(x:Customer) WHERE x <> keep
OPTIONAL MATCH (y:Customer)-[inc:REFERRED]->(dup) WHERE y <> keep
FOREACH (_ IN CASE WHEN x IS NULL THEN [] ELSE [1] END | MERGE (keep)-[:REFERRED]->(x))
FOREACH (_ IN CASE WHEN y IS NULL THEN [] ELSE [1] END | MERGE (y)-[:REFERRED]->(keep))
DELETE out, inc;

// name: drop_duplicate
MATCH (dup:Customer {id: $dup})
DETACH DELETE dup;
