// Depots no trunk line reaches.
MATCH (d:Depot) WHERE NOT (d)<-[:TRUNK]-()
RETURN d.code AS depot ORDER BY depot;
