// Factories that two or more of our direct suppliers depend on.
MATCH (s:Supplier)-[:SOURCES_FROM*1..4]->(f:Factory)
WITH f, collect(DISTINCT s.code) AS suppliers
WHERE size(suppliers) >= 2
RETURN f.code AS factory, suppliers ORDER BY size(suppliers) DESC;
