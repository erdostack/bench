CREATE CONSTRAINT species_id IF NOT EXISTS FOR (s:Species) REQUIRE s.id IS UNIQUE;
CREATE INDEX species_level IF NOT EXISTS FOR (s:Species) ON (s.trophic_level);
