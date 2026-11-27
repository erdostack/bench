// name: order_with_lines
MATCH (o:PurchaseOrder {number: $number})-[:TO]->(s:Supplier)
MATCH (o)-[l:LINE]->(p:Product)
RETURN o.number AS number, o.placed_on AS placed_on, s.name AS supplier,
       l.line_no AS line_no, p.sku AS sku, p.name AS product, p.category AS category,
       l.qty AS qty, l.unit_price_cents AS unit_price_cents, p.retired_on AS product_retired_on
ORDER BY l.line_no;

// name: spend_by_supplier
MATCH (o:PurchaseOrder)-[:TO]->(s:Supplier)
WHERE o.placed_on >= $from AND o.placed_on < $to
MATCH (o)-[l:LINE]->(:Product)
RETURN s.code AS supplier_code, s.name AS supplier, sum(l.qty * l.unit_price_cents) AS spend_cents
ORDER BY spend_cents DESC;
