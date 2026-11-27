// Weekly cutover to catalog 2026.47 (2,430 stores).
MATCH (old:Catalog:Live)
MATCH (new:Catalog {version: '2026.47'})
MATCH (s:Store)-[r:SERVES_FROM]->(old)
DELETE r
CREATE (s)-[:SERVES_FROM]->(new)
WITH DISTINCT old, new
REMOVE old:Live
SET new:Live;
