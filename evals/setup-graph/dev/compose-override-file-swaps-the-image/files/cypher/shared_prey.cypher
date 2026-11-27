MATCH (a:Species)-[:EATS]->(prey:Species)<-[:EATS]-(b:Species)
WHERE a.name < b.name
RETURN a.name AS first, b.name AS second, collect(prey.name) AS shared
ORDER BY size(shared) DESC, first;
