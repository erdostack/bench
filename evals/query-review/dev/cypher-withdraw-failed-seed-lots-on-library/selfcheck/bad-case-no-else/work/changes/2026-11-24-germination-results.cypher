// SL-77
MATCH (l:Lot) WHERE l.germination < 60
CALL (l) { SET l.status = CASE WHEN NOT l.heritage THEN 'withdrawn' END } IN TRANSACTIONS OF 2000 ROWS;
