// Lots with no recorded parent that still have descendants from the last three seasons.
MATCH (root:Lot)
WHERE NOT EXISTS { (root)-[:GROWN_FROM]->(:Lot) }
MATCH (recent:Lot)-[:GROWN_FROM*1..12]->(root)
WHERE recent.year >= 2024
RETURN root.code AS founder, root.year AS since, count(DISTINCT recent) AS recent_lots
ORDER BY since;
