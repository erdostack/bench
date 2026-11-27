// 013: delete trees felled before 2024-01-01 (the public tree map still draws them). About 7,800 trees.
// Count before and after (0 after):
//   MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01') RETURN count(t);
MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01')
MATCH (t)-[r:ON_STREET|IN_WARD|OF_SPECIES|REPLACED_BY]->()
CALL (r) { DELETE r } IN TRANSACTIONS OF 5000 ROWS;

MATCH (old:Tree {status: 'felled'}) WHERE old.felledOn < date('2024-01-01')
MATCH ()-[x]->(old)
CALL (x) { DELETE x } IN TRANSACTIONS OF 5000 ROWS;

MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01')
CALL (t) { DELETE t } IN TRANSACTIONS OF 5000 ROWS;
