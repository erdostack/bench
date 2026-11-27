// name: move_stock
MATCH (closing:Depot {code: $closing}), (target:Depot {code: $target})
MATCH (closing)-[s:STOCKS]->(sku:Sku)
MERGE (target)-[t:STOCKS]->(sku)
  ON CREATE SET t.qty = 0
SET t.qty = t.qty + s.qty
DELETE s;

// name: move_staff
MATCH (closing:Depot {code: $closing}), (target:Depot {code: $target})
MATCH (p:Staff)-[b:BASED_AT]->(closing)
CREATE (p)-[:BASED_AT {since: date()}]->(target)
DELETE b;

// name: close_depot
MATCH (d:Depot {code: $closing})
WHERE NOT (d)-[:STOCKS]->() AND NOT ()-[:BASED_AT]->(d)
DETACH DELETE d
RETURN count(*) AS closed;
