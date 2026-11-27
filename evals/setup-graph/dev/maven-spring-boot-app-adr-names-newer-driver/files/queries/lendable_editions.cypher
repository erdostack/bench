// Editions branch $branch can lend: a copy on its shelves or one courier hop away.
MATCH (b:Branch {code: $branch})-[:COURIER*0..1]-(:Branch)-[:HOLDS]->(c:Copy {status: 'shelf'})-[:OF]->(e:Edition)
RETURN DISTINCT e.isbn AS isbn, e.title AS title ORDER BY title;
