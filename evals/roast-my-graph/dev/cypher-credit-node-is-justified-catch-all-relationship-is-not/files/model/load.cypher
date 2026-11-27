// name: load_credits
UNWIND $rows AS row
MATCH (p:Person {id: row.person_id})
MATCH (prod:Production {id: row.production_id})
MERGE (c:Credit {id: row.credit_id})
SET c.role = row.role, c.billing_order = row.billing_order
MERGE (p)-[:HOLDS]->(c)
MERGE (c)-[:ON]->(prod)
WITH c, row
WHERE row.character_id IS NOT NULL
MATCH (ch:Character {id: row.character_id})
MERGE (c)-[:PLAYS]->(ch);

// name: load_awards
UNWIND $rows AS row
MATCH (c:Credit {id: row.credit_id})
MERGE (a:Award {id: row.award_id})
SET a.name = row.name, a.year = row.year, a.won = row.won
MERGE (a)-[:HONOURS]->(c);

// name: load_related
UNWIND $rows AS row
MATCH (a:Person {id: row.from_id})
MATCH (b:Person {id: row.to_id})
MERGE (a)-[r:RELATED {kind: row.kind}]->(b)
SET r.since = row.since;
