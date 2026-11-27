// what: delete BORROWED returned before 2024-11-24
// why: privacy audit
// check: MATCH ()-[b:BORROWED]->() WHERE b.returnedOn < '2024-11-24' RETURN count(b);
MATCH (:Patron)-[b:BORROWED]->(:Item)
WHERE b.returnedOn < '2024-11-24'
CALL (b) {
  DELETE b
} IN TRANSACTIONS OF 10000 ROWS;
