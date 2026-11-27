MATCH (e:Entry:Archived) CALL (e) { SET e.feePaid = true } IN TRANSACTIONS OF 1000 ROWS;
