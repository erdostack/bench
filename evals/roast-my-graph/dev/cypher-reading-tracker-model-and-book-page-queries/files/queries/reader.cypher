// name: my_ratings
MATCH (u:Reader {id: $reader})-[:GAVE]->(r:Rating)-[:OF]->(b:Book)
RETURN b.id AS id, b.title AS title, r.stars AS stars, r.rated_at AS rated_at
ORDER BY rated_at DESC;

// name: rate
MATCH (u:Reader {id: $reader}), (b:Book {id: $book})
MERGE (u)-[:GAVE]->(r:Rating)-[:OF]->(b)
  ON CREATE SET r.id = randomUUID()
SET r.stars = $stars, r.rated_at = datetime();

// name: shelf
MATCH (u:Reader {id: $reader})-[s:SHELVED]->(b:Book)
WHERE s.shelf = $shelf
RETURN b.id AS id, b.title AS title, s.at AS at
ORDER BY at DESC;
