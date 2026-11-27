// 012 (HB-41): delete inspections from before 2023-01-01, except notifiable ones (docs/retention.md:
// kept for good for the standstill audit). Expect about 31,000 minus the notifiable ones.
// Count before and after:
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable' RETURN count(i);
WITH date('2023-01-01') AS cutoff
MATCH (i:Inspection WHERE i.inspectedOn < cutoff AND i.outcome IN ['clear', 'treated'])
CALL (i) {
  DETACH DELETE i
} IN TRANSACTIONS OF 290 ROWS;
