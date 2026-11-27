MATCH (c:OneTimeCode)
WHERE c.expiresAt < datetime()
CALL (c) { DETACH DELETE c } IN TRANSACTIONS OF 1000 ROWS;
CREATE (:ExpiryRun {at: datetime()});
