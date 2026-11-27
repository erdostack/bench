// name: region_revenue
MATCH (r:Region)<-[:InRegion]-(s:Shop)<-[:PlacedAt]-(o:CustomerOrder)-[c:Contains]->(p:Product)
WHERE o.placed_on >= $from AND o.placed_on < $to
RETURN r.code AS region, r.name AS name,
       count(DISTINCT o) AS orders,
       sum(c.qty) AS units,
       sum(o.total_cents) AS revenue_cents
ORDER BY revenue_cents DESC;

// name: shop_orders
MATCH (s:Shop)<-[:PlacedAt]-(o:CustomerOrder)
WHERE o.placed_on >= $from AND o.placed_on < $to
RETURN s.code AS shop, s.name AS name, count(o) AS orders, avg(o.total_cents) AS avg_basket_cents
ORDER BY orders DESC;

// name: top_products
MATCH (o:CustomerOrder)-[c:Contains]->(p:Product)
WHERE o.placed_on >= $from AND o.placed_on < $to
RETURN p.sku AS sku, p.name AS name, sum(c.qty) AS units, sum(c.line_cents) AS sales_cents
ORDER BY sales_cents DESC
LIMIT 50;

// name: category_mix
MATCH (r:Region)<-[:InRegion]-(s:Shop)<-[:PlacedAt]-(o:CustomerOrder)-[c:Contains]->(p:Product)
WHERE o.placed_on >= $from AND o.placed_on < $to
RETURN r.code AS region, p.category AS category, sum(c.line_cents) AS sales_cents
ORDER BY region, sales_cents DESC;
