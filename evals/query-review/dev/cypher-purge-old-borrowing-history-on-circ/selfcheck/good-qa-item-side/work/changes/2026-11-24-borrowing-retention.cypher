// what: delete BORROWED returned before 2024-11-24 of patrons with keepHistory = false
// why: privacy audit, two-year retention (docs/privacy.md)
// check: MATCH (p:Patron {keepHistory: false})-[b:BORROWED]->() WHERE b.returnedOn < '2024-11-24' RETURN count(b);
MATCH (i:Item)<-[b:BORROWED]-(p:Patron)
WHERE p.keepHistory <> true AND b.returnedOn < '2024-11-24'
WITH b
CALL (b) { DELETE b } IN TRANSACTIONS OF 2000 ROWS
