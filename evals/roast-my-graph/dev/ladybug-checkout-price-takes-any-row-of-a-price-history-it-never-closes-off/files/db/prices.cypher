// name: price_at_checkout
MATCH (p:Product)-[x:PricedOn]->(l:PriceList)<-[:UsesList]-(s:School)
WHERE p.sku = $sku AND s.code = $school AND x.valid_from <= $today
RETURN x.price_cents AS price_cents
LIMIT 1;

// name: price_history
MATCH (p:Product)-[x:PricedOn]->(l:PriceList)
WHERE p.sku = $sku AND l.code = $list
RETURN x.price_cents AS price_cents, x.valid_from AS valid_from, x.valid_to AS valid_to
ORDER BY x.valid_from;

// name: list_export
MATCH (p:Product)-[x:PricedOn]->(l:PriceList)
WHERE l.code = $list AND x.valid_from <= $day AND (x.valid_to IS NULL OR x.valid_to >= $day)
RETURN p.sku AS sku, p.name AS name, x.price_cents AS price_cents
ORDER BY p.sku;

// name: close_current_price
MATCH (p:Product)-[x:PricedOn]->(l:PriceList)
WHERE p.sku = $sku AND l.code = $list AND x.valid_to IS NULL
SET x.valid_to = $day_before;

// name: add_price
MATCH (p:Product), (l:PriceList)
WHERE p.sku = $sku AND l.code = $list
CREATE (p)-[:PricedOn {price_cents: $price_cents, valid_from: $from, valid_to: NULL}]->(l);
