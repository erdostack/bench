-- Postgres 16. Loaded from the wiki's nightly dump.
CREATE TABLE page (
  id        bigint PRIMARY KEY,
  title     text NOT NULL UNIQUE,
  namespace int NOT NULL DEFAULT 0
);

CREATE TABLE link (
  from_id bigint NOT NULL REFERENCES page(id),
  to_id   bigint NOT NULL REFERENCES page(id),
  PRIMARY KEY (from_id, to_id)
);

CREATE INDEX link_to ON link (to_id);
