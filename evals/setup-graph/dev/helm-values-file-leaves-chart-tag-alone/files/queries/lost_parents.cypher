// Varieties with a parent line we no longer hold seed for.
MATCH (v:Variety)-[:BRED_FROM]->(p:Variety)
WHERE NOT (p)-[:STORED_AS]->(:Lot)
RETURN v.name AS variety, p.name AS missing_parent
ORDER BY variety;
