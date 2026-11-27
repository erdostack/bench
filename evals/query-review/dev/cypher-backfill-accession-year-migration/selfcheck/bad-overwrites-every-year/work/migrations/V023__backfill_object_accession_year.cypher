// migrate: autocommit
MATCH (o:Object)
CALL (o) {
  SET o.accessionYear = toInteger(substring(o.accessionNumber, 0, 4))
} IN TRANSACTIONS OF 50000 ROWS;
