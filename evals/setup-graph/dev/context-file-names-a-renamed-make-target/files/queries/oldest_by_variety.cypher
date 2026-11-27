MATCH (t:Tree)-[:OF_VARIETY]->(v:Variety)
WITH v, min(t.planted) AS first_planted, count(t) AS trees
RETURN v.name AS variety, first_planted, trees
ORDER BY first_planted;
