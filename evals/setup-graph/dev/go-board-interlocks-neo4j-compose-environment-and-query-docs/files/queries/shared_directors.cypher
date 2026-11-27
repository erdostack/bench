// Companies that share at least one sitting director with the given company.
MATCH (c:Company {id: $company})<-[:SITS_ON {current: true}]-(p:Person)-[:SITS_ON {current: true}]->(other:Company)
WHERE other <> c
RETURN other.id, other.name, collect(DISTINCT p.name) AS sharedDirectors
ORDER BY size(sharedDirectors) DESC, other.name;
