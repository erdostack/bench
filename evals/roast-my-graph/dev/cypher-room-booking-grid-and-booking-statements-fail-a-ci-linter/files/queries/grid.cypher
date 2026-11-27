// name: free_grid
MATCH (r:Room)-[:ON_FLOOR]->(f:Floor)-[:IN]->(:Building {code: $building})
MATCH (s:Slot)
OPTIONAL MATCH (r)<-[:FOR_ROOM]-(b:Booking {day: $day})-[:AT]->(s)
RETURN f.level AS level, r.name AS room, s.start AS slot, b IS NULL AS free
ORDER BY level, room, slot;
