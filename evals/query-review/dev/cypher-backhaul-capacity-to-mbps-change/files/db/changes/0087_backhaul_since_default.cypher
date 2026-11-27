// NET-298: links imported before 2019 have no `since`.
MATCH ()-[l:BACKHAUL]->()
WHERE l.since IS NULL
CALL (l) {
  SET l.since = date('2019-01-01')
} IN TRANSACTIONS OF 10000 ROWS;
