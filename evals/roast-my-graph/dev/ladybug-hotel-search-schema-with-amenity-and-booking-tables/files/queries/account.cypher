// name: my_stays
MATCH (g:Guest {id: $guest})-[:MADE]->(b:Booking)-[:AT_HOTEL]->(h:Hotel)
OPTIONAL MATCH (r:Review)-[:ABOUT_STAY]->(b)
RETURN b.id AS booking, h.name AS hotel, b.check_in AS check_in, b.nights AS nights, r.stars AS my_stars
ORDER BY check_in DESC;

// name: hotel_reviews
MATCH (r:Review)-[:ABOUT_STAY]->(b:Booking)-[:AT_HOTEL]->(h:Hotel {code: $hotel})
RETURN r.stars AS stars, r.body AS body, b.check_in AS stayed
ORDER BY stayed DESC
LIMIT 20;
