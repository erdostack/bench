// 0042: archive, batched
MATCH (s:Station)
WHERE s.status = 'decommissioned' AND s.decommissionedOn < date({year: 2025, month: 1, day: 1})
CALL (s) { SET s:ArchivedStation REMOVE s:Station } IN TRANSACTIONS OF 1000 ROWS;
