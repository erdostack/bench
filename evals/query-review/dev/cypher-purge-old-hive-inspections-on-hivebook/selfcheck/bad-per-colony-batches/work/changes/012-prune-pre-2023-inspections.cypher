// 012 (HB-41): delete inspections from before 2023-01-01, except notifiable ones (docs/retention.md:
// kept for good for the standstill audit). Expect about 31,000 minus the notifiable ones.
// Count before and after:
//   MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable' RETURN count(i);
MATCH (c:Colony)
CALL (c) {
  MATCH (i:Inspection)-[:OF]->(c)
  WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable'
  DETACH DELETE i
} IN TRANSACTIONS OF 100 ROWS;
