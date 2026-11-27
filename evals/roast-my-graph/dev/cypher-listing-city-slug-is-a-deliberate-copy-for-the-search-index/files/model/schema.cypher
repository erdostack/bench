CREATE CONSTRAINT listing_id IF NOT EXISTS FOR (l:Listing) REQUIRE l.id IS UNIQUE;
CREATE CONSTRAINT city_slug IF NOT EXISTS FOR (c:City) REQUIRE c.slug IS UNIQUE;
CREATE CONSTRAINT host_id IF NOT EXISTS FOR (h:Host) REQUIRE h.id IS UNIQUE;
CREATE CONSTRAINT amenity_code IF NOT EXISTS FOR (a:Amenity) REQUIRE a.code IS UNIQUE;

CREATE INDEX listing_city_price IF NOT EXISTS FOR (l:Listing) ON (l.city_slug, l.nightly_price);
