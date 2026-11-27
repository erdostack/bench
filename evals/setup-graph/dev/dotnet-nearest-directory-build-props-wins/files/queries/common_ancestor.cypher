MATCH (a:Language {code: $a})<-[:PARENT_OF*]-(anc:Language)-[:PARENT_OF*]->(b:Language {code: $b})
RETURN anc.name LIMIT 1;
