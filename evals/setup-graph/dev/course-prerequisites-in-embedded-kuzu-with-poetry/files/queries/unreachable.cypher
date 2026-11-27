// Courses that require something no course leads to (a missing entry course).
MATCH (c:Course)
WHERE NOT EXISTS { MATCH (c)-[:REQUIRES]->(:Course) } AND NOT EXISTS { MATCH (:Course)-[:REQUIRES]->(c) }
RETURN c.code ORDER BY c.code;
