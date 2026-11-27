// 012 (HB-41): prune inspections from before 2023 that are not notifiable.
// Retention (docs/retention.md): an inspection before 2023-01-01 may be removed, except outcome 'notifiable', which is kept for good.
// Removes each matching Inspection with its OF, CARRIED_OUT and NOTED relationships (up to 16 per inspection).
// Expect about 31,000 inspections before 2023 (docs/model.md), fewer once the notifiable ones are excluded.
// Count before and after:
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable' RETURN count(i);
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome = 'notifiable' RETURN count(i);
// Batches of 290 inspections: at most 290 x (1 node + 16 relationships) = 4,930 per transaction, under the 5,000 limit.
// Not yet reviewed. Run by the register secretary with bin/hb --file changes/012-prune-inspections-before-2023.cypher
MATCH (i:Inspection)
WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable'
CALL (i) {
  DETACH DELETE i
} IN TRANSACTIONS OF 290 ROWS;
