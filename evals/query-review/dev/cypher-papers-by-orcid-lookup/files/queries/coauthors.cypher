// People who share at least one paper with the author, most shared papers first.
// Parameters: $authorId (integer)
// Returns: authorId, name, sharedPapers
MATCH (a:Author {authorId: $authorId})-[:WROTE]->(p:Paper)<-[:WROTE]-(co:Author)
WHERE co <> a
RETURN co.authorId AS authorId, co.name AS name, count(p) AS sharedPapers
ORDER BY sharedPapers DESC, name
LIMIT 50;
