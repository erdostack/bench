// every border once, longest first
MATCH (a:Municipality)-[r:BORDERS]-(b:Municipality)
WHERE a.code < b.code
RETURN a.name, b.name, r.length_km
ORDER BY r.length_km DESC;
