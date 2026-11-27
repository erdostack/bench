MATCH (s:Substation {id: $substation_id})-[:SUPPLIES]->(f:Feeder)
RETURN f.id, f.name, f.voltage_kv
ORDER BY f.name;
