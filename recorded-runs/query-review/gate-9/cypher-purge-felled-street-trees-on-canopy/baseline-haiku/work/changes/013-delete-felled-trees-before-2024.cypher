// 013: delete the trees felled before 2024-01-01, which the public tree map draws as grey dots (request from the
// tree map owners). Each is removed with DETACH DELETE, so its relationships go too: INSPECTED (the inspection
// history of those trees), REPLACED_BY, ON_STREET, IN_WARD and OF_SPECIES. The planted replacements are not touched.
// Expect about 7,800 trees (docs/model.md). Count before, and record the result in the PR:
//   MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01')
//   OPTIONAL MATCH (t)-[r]-() RETURN count(DISTINCT t) AS trees, count(DISTINCT r) AS relationships;
// Count after, expect 0 trees:
//   MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01') RETURN count(t);
// Batches of 100 trees: a tree has at most 43 relationships, so a batch changes at most 100 x 44 = 4,400 items,
// under the 5,000 per transaction in docs/changes.md. Not yet reviewed: this file is a draft for the PR.
MATCH (t:Tree {status: 'felled'})
WHERE t.felledOn < date('2024-01-01')
CALL (t) {
  DETACH DELETE t
} IN TRANSACTIONS OF 100 ROWS;
