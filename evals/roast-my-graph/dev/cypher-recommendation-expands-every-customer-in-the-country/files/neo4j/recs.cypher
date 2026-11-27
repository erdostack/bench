// name: product_card
MATCH (p:Product {sku: $sku})-[:IN_CATEGORY]->(c:Category)
RETURN p.sku AS sku, p.title AS title, p.price_cents AS price_cents, c.slug AS category;

// name: recently_viewed
MATCH (me:Customer {id: $customer_id})-[v:VIEWED]->(p:Product)
RETURN p.sku AS sku, p.title AS title
ORDER BY v.at DESC
LIMIT 12;

// name: buy_again
MATCH (me:Customer {id: $customer_id})-[b:BOUGHT]->(p:Product)
RETURN p.sku AS sku, p.title AS title, max(b.at) AS last_bought
ORDER BY last_bought DESC
LIMIT 12;

// name: popular_near_you
// what people in the shopper's country have been buying lately
MATCH (me:Customer {id: $customer_id})-[:LIVES_IN]->(:Country)<-[:LIVES_IN]-(peer:Customer)-[b:BOUGHT]->(p:Product)
WHERE b.at >= $since
RETURN p.sku AS sku, p.title AS title, count(*) AS buys
ORDER BY buys DESC
LIMIT 10;

// name: category_bestsellers
MATCH (c:Category {slug: $slug})<-[:IN_CATEGORY]-(p:Product)
RETURN p.sku AS sku, p.title AS title, p.units_sold AS units_sold
ORDER BY p.units_sold DESC
LIMIT 20;
