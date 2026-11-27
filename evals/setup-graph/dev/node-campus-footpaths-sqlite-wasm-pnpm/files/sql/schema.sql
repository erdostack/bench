CREATE TABLE junction (
  id        TEXT PRIMARY KEY,
  kind      TEXT NOT NULL CHECK (kind IN ('door', 'junction', 'lift')),
  building  TEXT,
  level     INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE segment (
  from_id   TEXT NOT NULL REFERENCES junction(id),
  to_id     TEXT NOT NULL REFERENCES junction(id),
  metres    REAL NOT NULL,
  step_free INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY (from_id, to_id)
);
CREATE INDEX segment_to ON segment(to_id);
