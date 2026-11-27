// name: zone_rollup
// Assets by kind under a zone at any level, for the regulator's quarterly return.
MATCH (z:Zone {code: $zone_code})<-[:WITHIN*0..]-(block:Zone)<-[:LOCATED_IN]-(a:Asset)
RETURN a.kind AS kind, count(a) AS assets
ORDER BY kind;

// name: busiest_transformers
MATCH (t:Transformer)-[:SUPPLIES]->(m:Meter)
RETURN t.tag AS tag, t.rating_kva AS rating_kva, count(m) AS meters
ORDER BY meters DESC
LIMIT 50;

// name: overdue_work
MATCH (w:WorkOrder)-[:ON]->(a:Asset)
WHERE w.closed_ms IS NULL AND w.due_ms < $now_ms
RETURN w.id AS id, w.kind AS kind, a.tag AS asset, w.due_ms AS due_ms
ORDER BY w.due_ms;

// name: old_transformers
MATCH (t:Transformer)
WHERE t.installed_ms < $before_ms
RETURN t.tag AS tag, t.installed_ms AS installed_ms, t.rating_kva AS rating_kva
ORDER BY t.installed_ms;
