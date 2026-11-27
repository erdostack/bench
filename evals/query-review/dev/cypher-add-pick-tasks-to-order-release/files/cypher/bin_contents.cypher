// What is in a bin right now.
// Parameters: $binCode
// Returns: sku, name, qty
MATCH (p:Product)-[s:STORED_IN]->(:Bin {code: $binCode})
WHERE s.qty > 0
RETURN p.sku AS sku, p.name AS name, s.qty AS qty
ORDER BY sku;
