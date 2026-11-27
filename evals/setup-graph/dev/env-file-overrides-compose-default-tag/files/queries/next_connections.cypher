// Sailings you can still catch from a port after arriving there at a given time.
MATCH (p:Port {code: coalesce($port, 'SKA')})<-[:DEPARTS_FROM]-(s:Sailing)-[:ARRIVES_AT]->(dest:Port)
WHERE s.departs >= localtime(coalesce($after, '00:00')) + duration({minutes: coalesce($buffer, 12)})
RETURN s.id AS sailing, s.departs AS departs, dest.name AS to
ORDER BY departs
LIMIT 10;
