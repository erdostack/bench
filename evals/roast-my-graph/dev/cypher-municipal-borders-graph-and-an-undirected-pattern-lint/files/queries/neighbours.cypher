MATCH (m:Municipality {code: $code})-[r:BORDERS]-(n:Municipality)
RETURN n.code, n.name, r.length_km
ORDER BY n.name;
