// name: load_hotels
UNWIND $rows AS row
MERGE (h:Hotel {code: row.hotel_code})
SET h.name = row.name, h.city = row.city, h.stars = toInteger(row.stars);

// name: load_rooms
UNWIND $rows AS row
MATCH (h:Hotel {code: row.hotel_code})
MERGE (r:Room {number: row.number})
SET r.floor = toInteger(row.floor),
    r.beds = toInteger(row.beds),
    r.rate_class = row.rate_class
MERGE (r)-[:IN]->(h);
