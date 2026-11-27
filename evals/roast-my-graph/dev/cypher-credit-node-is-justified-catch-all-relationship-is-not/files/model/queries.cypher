// name: filmography
MATCH (p:Person {id: $person_id})-[:HOLDS]->(c:Credit)-[:ON]->(prod:Production)
RETURN prod.title AS title, prod.year AS year, c.role AS role
ORDER BY prod.year DESC;

// name: awards_for_performance
MATCH (p:Person {id: $person_id})-[:HOLDS]->(c:Credit)-[:ON]->(prod:Production {id: $production_id})
MATCH (a:Award)-[:HONOURS]->(c)
RETURN c.role AS role, a.name AS award, a.year AS year, a.won AS won
ORDER BY a.year;

// name: who_played
MATCH (ch:Character {id: $character_id})<-[:PLAYS]-(c:Credit)<-[:HOLDS]-(p:Person)
MATCH (c)-[:ON]->(prod:Production)
RETURN p.name AS actor, prod.title AS title, prod.year AS year
ORDER BY prod.year;

// name: family
MATCH (p:Person {id: $person_id})-[r:RELATED]-(q:Person)
WHERE r.kind IN ['spouse', 'sibling', 'parent']
RETURN q.name AS name, r.kind AS relation;

// name: represented_by
MATCH (p:Person {id: $person_id})-[r:RELATED]->(agent:Person)
WHERE r.kind = 'agent'
RETURN agent.name AS agent, r.since AS since;
