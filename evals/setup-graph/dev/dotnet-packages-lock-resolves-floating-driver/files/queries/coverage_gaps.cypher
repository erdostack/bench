MATCH (a:Site)-[r:ROAD]->(b:Site)
WHERE NOT EXISTS { (a)-[:HAS]->(:Charger {fast: true}) } AND NOT EXISTS { (b)-[:HAS]->(:Charger {fast: true}) }
RETURN a.name, b.name, r.km ORDER BY r.km DESC LIMIT 20;
