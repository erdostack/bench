// ticket: AGM Oct 2026 retention rule (docs/retention.md): delete plays aired before 2024-01-01 with their relationships. Not yet reviewed; to be run by the tech rota.
// Question for reviewer: is wq's runner sending this as an implicit (auto-commit) transaction? CALL { } IN TRANSACTIONS fails inside an explicit one.
// Cypher 5 syntax, Neo4j 5.26 (CALL (p) { } scope clause needs 5.23+).
// Limit: 5,000 nodes+relationships per transaction (docs/server.md). A play is 1 node + at most 7 relationships = 8, so 500 plays <= 4,000.
// Tracks, shows, presenters and Return nodes are not touched.
MATCH (p:Play)
WHERE p.airedOn < date('2024-01-01')
CALL (p) {
  DETACH DELETE p
} IN TRANSACTIONS OF 500 ROWS;
