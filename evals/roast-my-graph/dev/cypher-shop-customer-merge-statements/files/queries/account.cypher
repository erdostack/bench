// name: account_overview
MATCH (c:Customer {id: $id})
OPTIONAL MATCH (c)-[:PLACED]->(o:Order)
OPTIONAL MATCH (c)-[s:SUBSCRIBED_TO]->(p:Plan)
RETURN c.name AS name, count(DISTINCT o) AS orders, collect(DISTINCT p.code) AS plans;

// name: product_reviews
MATCH (p:Product {sku: $sku})<-[:OF]-(r:Review)<-[:WROTE]-(c:Customer)
RETURN c.name AS author, r.stars AS stars, r.text AS text
ORDER BY r.written_at DESC
LIMIT 20;
