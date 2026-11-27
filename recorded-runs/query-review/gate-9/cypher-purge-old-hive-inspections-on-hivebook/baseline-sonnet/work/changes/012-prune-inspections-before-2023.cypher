// 012 (HB-41): retention. Removes inspections from before 2023-01-01, except notifiable ones, which are
// kept for good (docs/retention.md). The ticket's statement would also have deleted the notifiable ones,
// so it is narrowed here. Expect about 31,000 inspections less the notifiable ones; the exact figure is
// the "to delete" count below. Colonies, apiaries, members and conditions are not touched; only the
// inspections and their OF, CARRIED_OUT and NOTED relationships go.
// Batch size: an inspection has at most 16 relationships, so at most 17 deleted items per row.
// 250 rows is at most 4,250 per transaction, inside the 5,000 limit (docs/changes.md).
// Counts before and after (to delete should go to 0; notifiable kept should not change):
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable' RETURN count(i) AS toDelete;
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome = 'notifiable' RETURN count(i) AS notifiableKept;
// Not yet reviewed or run. To be reviewed in a pull request and run by the register secretary with
// bin/hb --file changes/012-prune-inspections-before-2023.cypher
MATCH (i:Inspection)
WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable'
CALL (i) {
  DETACH DELETE i
} IN TRANSACTIONS OF 250 ROWS;
