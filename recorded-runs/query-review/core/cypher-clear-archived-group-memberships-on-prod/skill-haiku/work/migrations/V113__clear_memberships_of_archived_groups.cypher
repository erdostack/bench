// V113: remove the HAS_MEMBER relationships of archived groups. docs/forums.md says a group's memberships are
// removed when it is archived; they were not cleared for the 44 groups archived so far, so archived groups still
// appear in people's "your groups" lists. Forums, posts, comments, HAS_MODERATOR and HAS_TAG are kept.
// Expected: about 290,000 relationships (docs/forums.md, an estimate; the count below gives the exact figure).
// Count before and after (read-only, safe on prod):
//   MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person) RETURN count(m);   -- before: N, after: 0
//   MATCH (f:Forum {archived: true}) RETURN count(f);                              -- 44 before and after
// Batched because the repo limit (docs/data-changes.md) is 10,000 deletes per transaction on prod.
// Re-running is safe: the MATCH selects only relationships that still exist, so a rerun deletes the rest.
MATCH (:Forum {archived: true})-[m:HAS_MEMBER]->(:Person)
CALL (m) {
  DELETE m
} IN TRANSACTIONS OF 5000 ROWS;
