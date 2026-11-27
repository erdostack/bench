// step 2: drop the Member label from the tagged ones
MATCH (m:Member:FormerMember)
CALL (m) { REMOVE m:Member } IN TRANSACTIONS OF 2000 ROWS;
