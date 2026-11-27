// 013: DRAFT, NOT REVIEWED, NOT RUN. Delete trees felled before 2024-01-01 (status 'felled', felledOn < 2024-01-01)
// so the public tree map stops drawing them. DETACH DELETE also removes each tree's ON_STREET, IN_WARD, OF_SPECIES,
// INSPECTED (up to 38) and REPLACED_BY relationships, so their inspection history and replacement links are lost for
// good. There is no copy of canopy to try this on. Decide that is wanted before review.
// Expect about 7,800 trees (docs/model.md), up to 43 relationships each (about 336,000 nodes and relationships in all).
// A tree plus its relationships is at most 44, so 100 trees per transaction is at most 4,400, inside the 5,000 limit.
// Count before (expect about 7,800) and after (expect 0):
//   MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01') RETURN count(t);
// Also count before and after (should drop by the same number of trees' relationships only):
//   MATCH (t:Tree) RETURN count(t);
//   MATCH (:Tree {status: 'felled'})-[r:REPLACED_BY]-() WHERE r IS NOT NULL RETURN count(r);
MATCH (t:Tree {status: 'felled'})
WHERE t.felledOn < date('2024-01-01')
CALL (t) {
  DETACH DELETE t
} IN TRANSACTIONS OF 100 ROWS;
