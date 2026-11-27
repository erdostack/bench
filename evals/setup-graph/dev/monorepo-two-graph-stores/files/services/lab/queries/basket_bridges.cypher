// Products bought together with products from at least three different categories.
MATCH (p:Product)-[:BOUGHT_WITH]-(q:Product)
WITH p, count(DISTINCT q.category) AS categories
WHERE categories >= 3
RETURN p.sku AS sku, categories
ORDER BY categories DESC, sku;
