// name: upsert_hosts
UNWIND $hosts AS row
MERGE (h:Host {name: row.name})
SET h.serial = row.serial, h.os = row.os
WITH h, row
WHERE row.rack IS NOT NULL
MERGE (r:Rack {code: row.rack})
MERGE (h)-[:MOUNTED_IN]->(r);

// name: upsert_services
UNWIND $services AS row
MERGE (s:Service {name: row.name})
SET s.tier = row.tier
MERGE (t:Team {slug: row.team})
MERGE (t)-[:OWNS]->(s);

// name: upsert_instances
UNWIND $instances AS row
MATCH (s:Service {name: row.service})
MATCH (h:Host {name: row.host})
MERGE (s)-[:RUNS_ON]->(h);

// name: upsert_calls
UNWIND $calls AS row
MATCH (a:Service {name: row.caller})
MATCH (b:Service {name: row.callee})
MERGE (a)-[:DEPENDS_ON]->(b);
