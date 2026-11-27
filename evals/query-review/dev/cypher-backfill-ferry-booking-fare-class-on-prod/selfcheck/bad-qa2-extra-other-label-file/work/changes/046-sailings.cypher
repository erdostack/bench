MATCH (s:Sailing) CALL (s) { SET s.reported = true } IN TRANSACTIONS OF 1000 ROWS;
