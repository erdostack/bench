// name: create_listing
MATCH (h:Host {id: $host_id})
MATCH (c:City {slug: $city})
CREATE (l:Listing {id: $id, title: $title, nightly_price: $nightly_price, sleeps: $sleeps,
                   city_slug: c.slug, created_at: datetime()})
CREATE (h)-[:OFFERS]->(l)
CREATE (l)-[:IN]->(c);

// name: set_price
MATCH (l:Listing {id: $id})
SET l.nightly_price = $nightly_price;

// name: add_amenity
MATCH (l:Listing {id: $id})
MATCH (a:Amenity {code: $amenity})
MERGE (l)-[:HAS]->(a);

// name: retire_listing
MATCH (l:Listing {id: $id})
DETACH DELETE l;
