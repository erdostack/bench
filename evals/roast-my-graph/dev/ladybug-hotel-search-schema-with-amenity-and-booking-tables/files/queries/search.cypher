// name: hotels_with_amenities
MATCH (h:Hotel)-[:OFFERS]->(ha:HotelAmenity)-[:OF_AMENITY]->(a:Amenity)
WHERE h.city = $city AND a.code IN $amenities
WITH h, count(DISTINCT a) AS matched
WHERE matched = size($amenities)
RETURN h.code AS code, h.name AS name
ORDER BY name
LIMIT 50;

// name: hotel_amenities
MATCH (h:Hotel {code: $hotel})-[:OFFERS]->(ha:HotelAmenity)-[:OF_AMENITY]->(a:Amenity)
RETURN a.label AS amenity, ha.fee_eur AS fee, ha.since AS since
ORDER BY amenity;
