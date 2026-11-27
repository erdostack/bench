// 0033: archive wagons that have left the fleet.
MATCH (w:Wagon {status: 'scrapped'}) SET w:ArchivedWagon REMOVE w:Wagon;
MATCH (w:Wagon {status: 'stored'}) SET w:ArchivedWagon REMOVE w:Wagon;
