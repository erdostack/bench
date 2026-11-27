// ticket: HOL-58 purge lapsed seat holds created before 2026-10-01 (agreed at ops review 2026-11-20); holds with a depositRef are kept for accounts' refund reconciliation (docs/holds.md); batches of 10,000 rows, under the 25,000 per-transaction limit
MATCH (:Customer)-[h:HOLDS]->(:Departure)
WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') AND h.depositRef IS NULL
CALL (h) {
  DELETE h
} IN TRANSACTIONS OF 10000 ROWS;
