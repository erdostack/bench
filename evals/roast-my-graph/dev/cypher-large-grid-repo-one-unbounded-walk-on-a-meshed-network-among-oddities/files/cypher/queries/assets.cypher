// name: asset_card
MATCH (a:Asset {tag: $tag})-[:LOCATED_IN]->(z:Zone)
RETURN a.tag AS tag, a.kind AS kind, a.rating_kva AS rating_kva, a.installed_ms AS installed_ms,
       z.code AS zone, z.name AS zone_name;

// name: asset_neighbours
MATCH (a:Asset {tag: $tag})-[c:CONNECTS]-(b:Asset)
RETURN b.tag AS tag, b.kind AS kind, c.cable_id AS cable, c.normally_open AS normally_open, c.length_m AS length_m
ORDER BY b.tag;

// name: assets_in_block
MATCH (z:Zone {code: $zone_code})<-[:LOCATED_IN]-(a:Asset)
RETURN a.tag AS tag, a.kind AS kind
ORDER BY a.kind, a.tag;

// name: open_work
MATCH (a:Asset {tag: $tag})<-[:ON]-(w:WorkOrder)
WHERE w.closed_ms IS NULL
RETURN w.id AS id, w.kind AS kind, w.due_ms AS due_ms
ORDER BY w.due_ms;

// name: asset_by_old_ref
// still used by the two GIS export scripts, a few calls a week
// MATCH (a:Asset) WHERE a.legacy_ref = $ref RETURN a.tag AS tag;
MATCH (a:Asset)
WHERE a.legacy_ref = $ref
RETURN a.tag AS tag, a.kind AS kind
LIMIT 1;
