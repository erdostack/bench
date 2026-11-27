// 012 (HB-41): delete inspections before 2023-01-01 except notifiable ones (docs/retention.md).
// Count: MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome IN ['clear', 'treated'] RETURN count(i);
MATCH (i:Inspection)
WHERE i.inspectedOn < date({year: 2023, month: 1, day: 1}) AND i.outcome IN ['clear', 'treated']
CALL (i) { DETACH DELETE i } IN TRANSACTIONS OF 250 ROWS;
