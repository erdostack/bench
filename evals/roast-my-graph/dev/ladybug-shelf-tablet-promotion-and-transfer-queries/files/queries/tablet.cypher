// name: store_promos
MATCH (s:Store), (p:Promo)
WHERE s.id = $store AND p.active = true AND p.starts <= $today AND p.ends >= $today
RETURN p.code AS code, p.title AS title, p.ends AS ends
ORDER BY p.ends;

// name: promo_items
MATCH (p:Promo {code: $code})-[:COVERS]->(x:Product)
RETURN x.sku AS sku, x.name AS name
ORDER BY x.name;

// name: low_stock
MATCH (s:Store {id: $store})-[k:STOCKS]->(x:Product)
WHERE k.qty < 5
RETURN x.sku AS sku, x.name AS name, k.qty AS qty
ORDER BY k.qty;

// name: transfer_distance
MATCH (a:Store), (b:Store)
WHERE a.id = $from AND b.id = $to
OPTIONAL MATCH (a)-[n:NEAR]->(b)
RETURN a.name AS from_store, b.name AS to_store, n.km AS km;
