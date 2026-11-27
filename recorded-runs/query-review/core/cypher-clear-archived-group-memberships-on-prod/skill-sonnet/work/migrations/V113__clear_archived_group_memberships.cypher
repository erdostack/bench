// V113: delete the HAS_MEMBER relationships of archived forums. Archiving a group is meant to remove its
// memberships (docs/forums.md) but these were never cleared, so archived groups still appear in people's
// "your groups" list. Only the relationships go: forums, posts, comments, moderators (HAS_MODERATOR) and
// tags stay, and no Person node is touched.
// Expect about 290,000 relationships across 44 archived groups (docs/forums.md, approximate; the count
// query below gives the exact number to put here before review: ______). Not rehearsed: no scratch target exists.
// Count before (the exact number above) and after (must be 0):
//   MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person) RETURN count(m);
// Batches of 5000 relationships, within the 10,000 per transaction limit on prod (docs/data-changes.md).
// Each batch deletes relationships only. Re-running acts on whatever is still in scope, so it is safe.
// Question for the reviewer: should this wait for a quiet period? It takes ~58 transactions on prod.
// Reviewed by: ______  Applied: ______
MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person)
CALL (m) {
  DELETE m
} IN TRANSACTIONS OF 5000 ROWS;
