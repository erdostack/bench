// SL-77: withdraw non-heritage lots under 60% (untested counted as 0)
MATCH (l:Lot) WHERE coalesce(l.germination, 0) < 60 AND NOT l.heritage
CALL (l) { SET l.status = 'withdrawn' } IN TRANSACTIONS OF 2000 ROWS;
