MATCH (t:Tree {tag: 'T-118'})-[:SCION_FROM*1..10]->(source:Tree)
RETURN source.tag AS tag, source.planted AS planted
ORDER BY planted;
