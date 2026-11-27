// Release an order to the floor and return what the picker's handheld lists for it.
// Parameters: $orderId
// Returns: line, sku, qty, bins
MATCH (o:Order {id: $orderId})
SET o.status = 'released', o.releasedAt = datetime()
WITH o
MATCH (o)-[:HAS_LINE]->(l:Line)-[:OF]->(p:Product)
OPTIONAL MATCH (p)-[s:STORED_IN]->(b:Bin)
WHERE s.qty > 0
RETURN l.no AS line, p.sku AS sku, l.qty AS qty, collect(b.code) AS bins
ORDER BY line;
