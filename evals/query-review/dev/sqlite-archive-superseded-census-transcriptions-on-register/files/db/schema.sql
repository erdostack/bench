CREATE TABLE entity (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,          -- person | record | volume
  label TEXT NOT NULL,
  year INTEGER
);
CREATE TABLE relation (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,          -- appears_in | parent_of | in_volume
  from_id INTEGER NOT NULL REFERENCES entity(id),
  to_id INTEGER NOT NULL REFERENCES entity(id),
  status TEXT NOT NULL,        -- current | superseded | disputed
  volunteer TEXT,
  created_on TEXT NOT NULL
);
CREATE TABLE relation_archive (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,
  from_id INTEGER NOT NULL,
  to_id INTEGER NOT NULL,
  status TEXT NOT NULL,
  volunteer TEXT,
  created_on TEXT NOT NULL
);
CREATE INDEX relation_from ON relation(from_id, kind);
CREATE INDEX relation_to ON relation(to_id, kind);
CREATE INDEX relation_status ON relation(kind, status);
