// 012 (HB-41): prune inspections from before 2023 that retention allows to go.
// Rule (docs/retention.md): an Inspection with inspectedOn before 2023-01-01 may be removed, except
// one whose outcome is 'notifiable'; those are kept for good (standstill audit, disease history).
// Ticket HB-41 asked for every pre-2023 inspection; this file leaves the notifiable ones in, as
// the retention rule requires. Colonies, apiaries, members and conditions are not removed.
// DETACH DELETE also removes each inspection's OF, CARRIED_OUT and NOTED relationships (at most 16
// per inspection). Batch of 294 inspections: 294 x (1 node + 16 relationships) = 4998, inside the
// 5,000 limit in docs/changes.md.
// Count before (should change N) and after (expect 0):
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable' RETURN count(i);
// Also check that notifiable pre-2023 inspections are untouched (count before and after must match):
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome = 'notifiable' RETURN count(i);
// Re-running is safe: it only acts on rows still in scope.
// Not yet run anywhere: no test copy of hivebook exists. Run by the register secretary under docs/changes.md.
MATCH (i:Inspection)
WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable'
CALL (i) {
  DETACH DELETE i
} IN TRANSACTIONS OF 294 ROWS;
