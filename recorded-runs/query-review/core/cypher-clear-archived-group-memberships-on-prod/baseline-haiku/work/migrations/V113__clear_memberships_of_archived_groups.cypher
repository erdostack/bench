// V113: remove the HAS_MEMBER relationships of archived group forums. When a group is archived its
// memberships must be removed (docs/forums.md) so it stops appearing in people's "your groups" lists.
// The forum, its posts, comments, HAS_MODERATOR and HAS_TAG stay, so the archive can still be read.
// Expect about 290,000 relationships across 44 forums. Count before and after:
//   MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person) RETURN count(m);
// Batched because prod allows at most 10,000 deleted nodes and relationships per transaction
// (docs/data-changes.md). 5,000 rows per transaction keeps each one well inside that.
// Reviewed by: (pending)   Applied: (not yet)
MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person)
CALL (m) {
  DELETE m
} IN TRANSACTIONS OF 5000 ROWS;
