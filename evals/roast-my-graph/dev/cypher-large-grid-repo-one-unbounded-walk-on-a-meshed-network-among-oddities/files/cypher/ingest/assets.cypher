// name: upsert_zones
// $rows is ordered by level, so a parent always exists before its children.
UNWIND $rows AS row
MERGE (z:Zone {code: row.code})
SET z.name = row.name, z.level = row.level
WITH z, row
WHERE row.parent_code IS NOT NULL
MATCH (parent:Zone {code: row.parent_code})
MERGE (z)-[:WITHIN]->(parent);

// name: upsert_assets
UNWIND $rows AS row
MERGE (a:Asset {tag: row.tag})
SET a.kind = row.kind,
    a.installed_ms = row.installed_ms,
    a.rating_kva = row.rating_kva,
    a.legacy_ref = row.legacy_ref
WITH a, row
MATCH (z:Zone {code: row.zone_code})
MERGE (a)-[:LOCATED_IN]->(z);

// name: label_substations
MATCH (a:Asset {kind: 'substation'}) SET a:Substation;

// name: label_transformers
MATCH (a:Asset {kind: 'transformer'}) SET a:Transformer;

// name: label_switches
MATCH (a:Asset {kind: 'switch'}) SET a:Switch;

// name: label_joints
MATCH (a:Asset {kind: 'joint'}) SET a:Joint;
