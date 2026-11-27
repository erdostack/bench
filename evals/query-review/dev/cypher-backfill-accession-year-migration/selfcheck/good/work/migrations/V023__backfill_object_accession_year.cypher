// migrate: autocommit
// Fill Object.accessionYear from the year that starts accessionNumber ("1987.214.3" -> 1987), for the
// objects that do not have it yet (about 5.1 million of 6.2 million, docs/model.md).
// One property per object; 50,000 objects per transaction stays under the 200,000 in docs/migrations.md.
// Re-runnable: an object that has its year no longer matches.
MATCH (o:Object)
WHERE o.accessionYear IS NULL AND o.accessionNumber =~ '[0-9]{4}[.].*'
CALL (o) {
  SET o.accessionYear = toInteger(substring(o.accessionNumber, 0, 4))
} IN TRANSACTIONS OF 50000 ROWS;
