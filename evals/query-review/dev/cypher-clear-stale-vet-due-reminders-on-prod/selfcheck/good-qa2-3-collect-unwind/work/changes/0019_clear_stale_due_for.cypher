// ticket: VX-90 clear stale DUE_FOR reminders due before 2025-01-01; GOT stays. Count: MATCH (:Pet)-[d:DUE_FOR]->(:Vaccine) WHERE d.dueOn < '2025-01-01' RETURN count(d);
MATCH (:Pet)-[d:DUE_FOR]->(:Vaccine) WHERE d.dueOn < '2025-01-01'
WITH collect(d) AS ds UNWIND ds AS x
CALL (x) { DELETE x } IN TRANSACTIONS OF 10000 ROWS;
