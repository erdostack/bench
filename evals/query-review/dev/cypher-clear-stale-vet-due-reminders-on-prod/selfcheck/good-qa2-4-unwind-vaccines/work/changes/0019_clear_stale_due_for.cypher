// ticket: VX-90 clear stale DUE_FOR reminders due before 2025-01-01; GOT stays. Count: MATCH (:Pet)-[d:DUE_FOR]->(:Vaccine) WHERE d.dueOn < '2025-01-01' RETURN count(d);
UNWIND ['DHP', 'LEPTO4', 'RCP', 'FeLV', 'RHD2'] AS code
MATCH (:Pet)-[d:DUE_FOR]->(:Vaccine {code: code}) WHERE d.dueOn < '2025-01-01'
CALL (d) { DELETE d } IN TRANSACTIONS OF 10000 ROWS;
