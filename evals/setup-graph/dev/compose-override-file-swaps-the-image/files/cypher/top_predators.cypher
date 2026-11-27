MATCH (s:Species)
WHERE NOT EXISTS { (:Species)-[:EATS]->(s) }
RETURN s.name AS species, s.trophic_level AS level
ORDER BY level DESC, species;
