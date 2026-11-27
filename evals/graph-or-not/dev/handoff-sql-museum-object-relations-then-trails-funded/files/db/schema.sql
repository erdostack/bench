-- Postgres 16, the collections database.
CREATE TABLE object (
  id            bigint PRIMARY KEY,
  accession_no  text NOT NULL UNIQUE,
  title         text NOT NULL,
  made_from     int,
  made_to       int
);

-- Curated relations between objects ("same workshop", "depicts", "pair of", ...). Stored once per pair.
CREATE TABLE relation (
  a_id     bigint NOT NULL REFERENCES object(id),
  b_id     bigint NOT NULL REFERENCES object(id),
  kind     text NOT NULL,
  added_by text NOT NULL,
  PRIMARY KEY (a_id, b_id, kind)
);

CREATE INDEX relation_b ON relation (b_id);
