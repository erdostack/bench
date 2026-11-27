// Every lot cut, directly or indirectly, from the recalled one.
MATCH (r:Lot {id: $lot})<-[:CUT_FROM*1..]-(child:Lot)
RETURN child.id AS lot
ORDER BY lot;
