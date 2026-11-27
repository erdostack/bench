// 012 (HB-41): purge
MATCH (i:Inspection)-[r]-() WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable'
CALL (r) { DELETE r } IN TRANSACTIONS OF 5000 ROWS;
MATCH (i:Inspection) WHERE i.inspectedOn < date('2023-01-01') AND i.outcome <> 'notifiable'
OPTIONAL MATCH (i)-[x]-() WITH i, x WHERE x IS NULL
CALL (i) { DELETE i } IN TRANSACTIONS OF 5000 ROWS;
