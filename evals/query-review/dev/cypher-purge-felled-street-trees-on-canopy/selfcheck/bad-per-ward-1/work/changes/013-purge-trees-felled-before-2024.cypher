// 013: delete trees felled before 2024-01-01 (the public tree map still draws them). About 7,800 trees.
// Count before and after (0 after):
//   MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01') RETURN count(t);
MATCH (wd:Ward)
CALL (wd) {
  MATCH (t:Tree)-[:IN_WARD]->(wd) WHERE t.status = 'felled' AND t.felledOn < date('2024-01-01')
  DETACH DELETE t
} IN TRANSACTIONS OF 1 ROW;
