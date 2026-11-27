// 0033: archive wagons that have left the fleet (scrapped or sold); workshop and stored wagons stay fleet.
MATCH (w:Wagon {status: 'scrapped'}) SET w:ArchivedWagon REMOVE w:Wagon;
MATCH (w:Wagon {status: 'sold'}) SET w:ArchivedWagon REMOVE w:Wagon;
