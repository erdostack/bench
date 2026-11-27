// ticket: clear stale DUE_FOR
MATCH (:Pet)<-[d:DUE_FOR]-(:Vaccine)
WHERE d.dueOn < '2025-01-01'
CALL (d) { DELETE d } IN TRANSACTIONS OF 10000 ROWS;
