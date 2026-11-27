// 0033: archive scrapped wagons.
MATCH (w:Wagon {status: 'scrapped'}) SET w:ArchivedWagon REMOVE w:Wagon;
