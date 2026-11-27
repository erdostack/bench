// 0012: delete the reminders sent before 2025-12-01 (about 6.3 million), to make the reminders list in the surgery screens load faster. Patients, practices and recalls are kept (docs/graph.md). Each reminder goes with its FOR, FROM and ABOUT relationships (2 to 3 each).
// Rule: every (:Reminder) with sentAt before 2025-12-01T00:00:00Z. The set is fixed by the request, so it is taken once.
// Count before (keep the numbers for the after comparison):
//   MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z') RETURN count(r);
//   MATCH (p:Patient) RETURN count(p);  MATCH (p:Practice) RETURN count(p);  MATCH (c:Recall) RETURN count(c);
//   MATCH (:Reminder)-[x]->() RETURN count(x);   // relationships on all reminders, to check the removed ones
// Expected: step 1 deletes about 6.3 million reminders and their relationships. Patient, Practice and Recall counts must not change.
// Count after (must be 0): MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z') RETURN count(r);
// Batched: a transaction on chairside deletes at most 3,000 entities, nodes and relationships together (docs/environments.md). A reminder counts as 1 node plus up to 3 relationships, so 500 reminders per transaction is at most 2,000 entities. Re-running is safe: deleted reminders no longer match.
// Engine: Neo4j 5.26. The CALL (r) scope form needs 5.23 or later; change 0011 uses it too.
// Cypher language: the database default (no CYPHER prefix).
// Status: NOT RUN. Production change, out of hours, by the practice systems on-call after review: bin/cs chairside --file changes/0012-delete-reminders-sent-before-2025-12.cypher
// Not checked with EXPLAIN and not counted: no copy of chairside exists that a workstation can reach.
// Reviewed by: (pending)
MATCH (r:Reminder)
WHERE r.sentAt < datetime('2025-12-01T00:00:00Z')
CALL (r) {
  DETACH DELETE r
} IN TRANSACTIONS OF 500 ROWS;
