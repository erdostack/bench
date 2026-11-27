// name: meters_without_reading
MATCH (m:Meter)
WHERE NOT EXISTS { MATCH (m)-[:RECORDED]->(r:Reading) WHERE r.month = $month }
RETURN m.serial AS meter
ORDER BY meter;

// name: meters_without_owner
MATCH (m:Meter)
WHERE NOT EXISTS { MATCH (:Customer)-[:OWNS]->(m) }
RETURN m.serial AS meter;
