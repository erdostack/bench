// name: book_cell
MATCH (r:Room {id: $room}), (s:Slot {start: $start}), (who:Person {id: $person})
CREATE (b:Booking {cell: $room + '|' + $day + '|' + $start, day: $day, created_at: datetime()})
CREATE (b)-[:FOR_ROOM]->(r), (b)-[:AT]->(s), (who)-[:BOOKED]->(b)
RETURN b.cell AS cell;

// name: cancel_cell
MATCH (who:Person {id: $person})-[:BOOKED]->(b:Booking {cell: $cell})
DETACH DELETE b;
