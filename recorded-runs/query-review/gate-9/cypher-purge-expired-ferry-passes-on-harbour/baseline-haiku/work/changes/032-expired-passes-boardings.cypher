// 032: remove the BOARDED relationships of passes that expired before 2026-01-01, so that
// step 033 can delete those passes. Renewals are done; the ramp check-in pass lookup is slow
// with these passes still in the graph. Expect about 38,000 passes; the BOARDED count is not yet known
// (about 3.1 million BOARDED in total). Run in batches of 5,000 relationships per transaction.
// Count before and after:
//   MATCH (p:Pass)-[b:BOARDED]->(:Sailing) WHERE p.validUntil < date('2026-01-01') RETURN count(b);
// Fare reports read BOARDED history: confirm with the fare-report owner before review that these
// boardings are not needed. This change cannot be undone from the graph; the backup is off-site.
// Not yet reviewed. Not run on harbour.
MATCH (p:Pass)-[b:BOARDED]->(:Sailing)
WHERE p.validUntil < date('2026-01-01')
CALL (b) {
  DELETE b
} IN TRANSACTIONS OF 5000 ROWS;
