// 0033: archive out-of-service wagons.
MATCH (w:Wagon) WHERE w.status <> 'active' SET w:ArchivedWagon REMOVE w:Wagon;
