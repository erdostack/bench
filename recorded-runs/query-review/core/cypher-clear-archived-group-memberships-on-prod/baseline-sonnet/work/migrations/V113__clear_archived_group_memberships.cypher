// V113: remove every HAS_MEMBER relationship from archived group forums. Archiving a group is meant to clear
// its memberships (docs/forums.md) but 44 archived groups were never cleared, so they still appear in
// people's "your groups" lists. The forums, posts, comments, moderators and tags are untouched.
// Expect about 290,000 relationships across 44 forums (largest about 26,000, smallest about 400); confirm the
// exact figure with the "before" count and re-check it on the day of release. Count before and after
// (after must be 0):
//   MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person) RETURN count(m);
//   MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person) RETURN count(DISTINCT f);
// Deletes run in batches of 5,000 rows, well inside the 10,000 per-transaction limit on prod.
// Not yet reviewed or applied: needs a pull request and the release job.
MATCH (f:Forum {archived: true})-[m:HAS_MEMBER]->(:Person)
CALL (m) {
  DELETE m
} IN TRANSACTIONS OF 5000 ROWS;
