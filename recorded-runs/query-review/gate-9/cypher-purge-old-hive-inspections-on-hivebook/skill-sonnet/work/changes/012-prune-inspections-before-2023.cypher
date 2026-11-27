// 012 (HB-41): retention prune. Deletes inspections from before 2023-01-01, except notifiable ones.
// Why: the colony history screen loads every inspection a colony ever had and is slow on old colonies;
// docs/retention.md keeps the current season and three before. An inspection with outcome 'notifiable'
// is kept for good (standstill audit, disease history), so it is excluded, which the ticket's statement
// does not do. Colonies, apiaries, members and conditions are not touched; only their links to the
// deleted inspections go.
// Expect about 31,000 inspections minus the notifiable ones, and up to 16 relationships each
// (docs/model.md). Fill in the exact number from the "before" count when the reviewer runs it.
// Batches of 250 inspections: at most 250 x (1 node + 16 relationships) = 4,250, inside the 5,000 limit
// of docs/changes.md.
// Count before (expect N) and after (expect 0); the kept-notifiable count must be the same before and after:
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable' RETURN count(i);
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome = 'notifiable' RETURN count(i);
// Neo4j 5.26 (Cypher 5); CALL (i) { } needs 5.23 or later. Run as an auto-commit statement, not inside an
// explicit transaction. Safe to re-run: it only acts on what is still in scope.
// Question for the reviewer: should any other old inspection be kept? 'outcome' is always set, so
// <> 'notifiable' cannot skip a row with a missing outcome.
// Reviewed by: (pending), run on hivebook by the register secretary.
MATCH (i:Inspection)
WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable'
CALL (i) {
  DETACH DELETE i
} IN TRANSACTIONS OF 250 ROWS;
