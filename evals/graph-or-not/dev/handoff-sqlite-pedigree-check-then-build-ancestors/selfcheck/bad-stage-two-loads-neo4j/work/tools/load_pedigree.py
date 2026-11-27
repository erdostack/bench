from neo4j import GraphDatabase

QUERY = 'MATCH (a:Animal {id: $id})-[:CHILD_OF*1..4]->(x) RETURN x.id'
