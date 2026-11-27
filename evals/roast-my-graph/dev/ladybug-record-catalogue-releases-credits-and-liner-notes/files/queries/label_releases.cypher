MATCH (r:Release)-[:RELEASED_BY]->(l:Label {id: $label_id})
RETURN r.id, r.title, r.year
ORDER BY r.year;
