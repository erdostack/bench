// Ports that cannot be reached from P001 at all.
MATCH (x:Port)
WHERE NOT EXISTS { MATCH (:Port {code: 'P001'})-[:SAILS_TO*1..12]->(x) } AND x.code <> 'P001'
RETURN x.code ORDER BY x.code;
