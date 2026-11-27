// Piers no route calls at any more.
MATCH (p:Pier) WHERE NOT (p)<-[:CALLS_AT]-()
RETURN p.name AS pier ORDER BY pier;
