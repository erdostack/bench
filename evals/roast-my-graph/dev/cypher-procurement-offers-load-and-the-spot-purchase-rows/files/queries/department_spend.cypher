MATCH (d:Department {code: $dept})-[o:ORDERED]->(p:Product)
WHERE o.on >= date($from) AND o.on < date($to)
RETURN p.gtin, p.name, sum(o.qty) AS qty, sum(o.qty * o.unit_price) AS spend
ORDER BY spend DESC
