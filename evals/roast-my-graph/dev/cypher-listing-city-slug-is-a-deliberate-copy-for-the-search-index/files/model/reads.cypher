// name: search_city
MATCH (l:Listing)
WHERE l.city_slug = $city AND l.nightly_price >= $min_price AND l.nightly_price <= $max_price
RETURN l.id AS id, l.title AS title, l.nightly_price AS nightly_price, l.sleeps AS sleeps
ORDER BY l.nightly_price
SKIP $offset LIMIT 24;

// name: listing_page
MATCH (h:Host)-[:OFFERS]->(l:Listing {id: $id})-[:IN]->(c:City)
OPTIONAL MATCH (l)-[:HAS]->(a:Amenity)
RETURN l.title AS title, l.nightly_price AS nightly_price, l.sleeps AS sleeps, c.name AS city, h.name AS host,
       collect(a.name) AS amenities;

// name: host_listings
MATCH (h:Host {id: $host_id})-[:OFFERS]->(l:Listing)
RETURN l.id AS id, l.title AS title, l.city_slug AS city, l.nightly_price AS nightly_price
ORDER BY l.created_at DESC;

// name: city_summary
MATCH (c:City {slug: $city})<-[:IN]-(l:Listing)
RETURN count(l) AS listings, avg(l.nightly_price) AS avg_price, min(l.nightly_price) AS min_price;
