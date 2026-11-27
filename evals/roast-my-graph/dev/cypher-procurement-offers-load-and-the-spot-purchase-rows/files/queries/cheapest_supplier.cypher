// cheapest current offer for a product
MATCH (s:Supplier)-[r:SUPPLIES]->(p:Product {gtin: $gtin})
WHERE r.updated >= date() - duration('P90D')
RETURN s.name, r.contract_ref, r.unit_price
ORDER BY r.unit_price
LIMIT 1
