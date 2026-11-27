LOAD CSV WITH HEADERS FROM 'file:///links.csv' AS row
CALL (row) { MERGE (a:Account {id: toInteger(row.account_id)}) MERGE (e:Entity {id: toInteger(row.entity_id)}) MERGE (a)-[:USED]->(e) } IN TRANSACTIONS OF 10000 ROWS;
