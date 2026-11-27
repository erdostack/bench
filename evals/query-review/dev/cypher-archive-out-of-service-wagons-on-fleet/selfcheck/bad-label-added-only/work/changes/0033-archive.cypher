// 0033: tag scrapped and sold wagons as archived.
MATCH (w:Wagon) WHERE w.status IN ['scrapped', 'sold'] SET w:ArchivedWagon;
