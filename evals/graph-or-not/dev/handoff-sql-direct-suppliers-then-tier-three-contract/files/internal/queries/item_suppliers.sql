-- Who delivers this item to us.
SELECT p.id, p.name, p.country
FROM supplies s
JOIN party p ON p.id = s.supplier_id
JOIN party us ON us.id = s.buyer_id AND us.kind = 'us'
WHERE s.item_id = $1
ORDER BY p.name;
