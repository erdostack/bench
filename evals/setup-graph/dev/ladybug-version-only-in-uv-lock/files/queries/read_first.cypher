// Everything the agenda paper builds on, up to three citations deep, oldest first.
MATCH (p:Paper {key: 'vale2024'})-[:CITES*1..3]->(earlier:Paper)
RETURN DISTINCT earlier.key AS key, earlier.title AS title, earlier.year AS year
ORDER BY year, key;
