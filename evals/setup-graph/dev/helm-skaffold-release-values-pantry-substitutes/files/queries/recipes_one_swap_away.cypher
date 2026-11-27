MATCH (r:Recipe)-[:USES]->(missing:Ingredient)-[:SUBSTITUTES_FOR]->(alt:Ingredient)
WHERE missing.name IN $missing
RETURN r.slug, collect(DISTINCT alt.name) AS swaps
LIMIT 25;
