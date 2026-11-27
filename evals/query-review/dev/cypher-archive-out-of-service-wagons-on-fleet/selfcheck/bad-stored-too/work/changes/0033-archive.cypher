// 0033: archive wagons not coming back soon (scrapped, sold, stored).
MATCH (w:Wagon) WHERE w.status IN ['scrapped', 'sold', 'stored'] SET w:ArchivedWagon REMOVE w:Wagon;
