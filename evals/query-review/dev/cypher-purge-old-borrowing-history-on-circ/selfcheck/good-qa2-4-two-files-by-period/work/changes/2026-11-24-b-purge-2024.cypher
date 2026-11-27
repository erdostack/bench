// what: delete BORROWED returned before 2024-11-24 of patrons with keepHistory = false
// why: privacy audit, two-year retention (docs/privacy.md)
// check: MATCH (p:Patron {keepHistory: false})-[b:BORROWED]->() WHERE b.returnedOn < '2024-11-24' RETURN count(b);
MATCH (p:Patron {keepHistory: false})-[b:BORROWED]->(:Item)
WHERE b.returnedOn >= '2024-01-01' AND b.returnedOn < '2024-11-24'
CALL (b) { DELETE b } IN TRANSACTIONS OF 10000 ROWS;
