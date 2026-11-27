// name: book_stars
MATCH (b:Book {id: $book})<-[:OF]-(r:Rating)
RETURN avg(r.stars) AS stars, count(r) AS ratings;

// name: loved_also_loved
MATCH (b:Book {id: $book})<-[:OF]-(r1:Rating)<-[:GAVE]-(u:Reader)-[:GAVE]->(r2:Rating)-[:OF]->(other:Book)
WHERE r1.stars >= 4 AND r2.stars >= 4 AND other <> b
RETURN other.id AS id, other.title AS title, count(u) AS readers
ORDER BY readers DESC
LIMIT 12;
