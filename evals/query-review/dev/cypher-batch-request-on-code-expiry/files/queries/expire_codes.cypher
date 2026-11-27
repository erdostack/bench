// Every minute (app/expiry.py): remove expired one-time codes and record the run (SEC-88).
MATCH (c:OneTimeCode)
WHERE c.expiresAt < datetime()
WITH collect(c) AS expired
CREATE (:ExpiryRun {at: datetime(), removed: size(expired)})
WITH expired
UNWIND expired AS c
DETACH DELETE c;
