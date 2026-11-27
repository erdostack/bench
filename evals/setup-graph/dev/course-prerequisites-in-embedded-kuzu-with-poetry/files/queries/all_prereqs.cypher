// Every course that must be passed before $code, at any depth.
MATCH (c:Course {code: $code})-[:REQUIRES*1..8]->(p:Course)
RETURN DISTINCT p.code, p.title
ORDER BY p.code;
