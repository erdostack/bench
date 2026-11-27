MATCH (p:Pollinator)-[:VISITED]->(pl:Plant)
RETURN p.taxon AS pollinator, count(DISTINCT pl) AS plants ORDER BY plants DESC LIMIT 10;
