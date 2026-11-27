// Wagons that cannot run if component $part is recalled.
MATCH (c:Component {part_no: $part})<-[:FITTED_WITH]-(b:Bogie)<-[:RIDES_ON]-(w:Wagon)
RETURN w.number AS wagon, b.serial AS bogie
ORDER BY wagon;
