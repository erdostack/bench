// Weekly cutover to catalog 2026.47 (2,430 stores).
MATCH (old:Catalog:Live)
MATCH (new:Catalog {version: '2026.47'})
MATCH (s:Store)-[r:SERVES_FROM]->(old)
CALL (s, r, new) {
  DELETE r
  CREATE (s)-[:SERVES_FROM]->(new)
} IN TRANSACTIONS OF 500 ROWS;
MATCH (old:Catalog:Live), (new:Catalog {version: '2026.47'})
REMOVE old:Live
SET new:Live;
