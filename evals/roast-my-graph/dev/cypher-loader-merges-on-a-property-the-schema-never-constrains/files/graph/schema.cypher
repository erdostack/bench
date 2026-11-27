CREATE CONSTRAINT artwork_catalogue_id IF NOT EXISTS FOR (a:Artwork) REQUIRE a.catalogue_id IS UNIQUE;
CREATE CONSTRAINT maker_id IF NOT EXISTS FOR (m:Maker) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT venue_code IF NOT EXISTS FOR (v:Venue) REQUIRE v.code IS UNIQUE;

CREATE INDEX artwork_department IF NOT EXISTS FOR (a:Artwork) ON (a.department);
CREATE INDEX maker_name IF NOT EXISTS FOR (m:Maker) ON (m.name);
