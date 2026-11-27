// name: free_rooms
MATCH (h:Hotel {code: $hotel})<-[:IN]-(r:Room)
WHERE r.beds >= $beds
  AND NOT EXISTS {
    MATCH (r)<-[:OF]-(b:Booking)
    WHERE b.check_in < date($to) AND b.check_out > date($from)
  }
RETURN r.number AS number, r.floor AS floor, r.beds AS beds, r.rate_class AS rate_class
ORDER BY r.number;

// name: book_room
MATCH (g:Guest {id: $guest_id})
MATCH (h:Hotel {code: $hotel})<-[:IN]-(r:Room {number: $number})
CREATE (b:Booking {ref: $ref, check_in: date($from), check_out: date($to)})
CREATE (g)-[:MADE]->(b)
CREATE (b)-[:OF]->(r);

// name: cancel_booking
MATCH (b:Booking {ref: $ref})
DETACH DELETE b;

// name: guest_bookings
MATCH (g:Guest {id: $guest_id})-[:MADE]->(b:Booking)-[:OF]->(r:Room)-[:IN]->(h:Hotel)
RETURN b.ref AS ref, h.name AS hotel, r.number AS room, b.check_in AS check_in, b.check_out AS check_out
ORDER BY b.check_in DESC;

// name: housekeeping_today
MATCH (h:Hotel {code: $hotel})<-[:IN]-(r:Room)<-[:OF]-(b:Booking)
WHERE b.check_out = date($day)
RETURN r.number AS number, r.floor AS floor
ORDER BY r.floor, r.number;
