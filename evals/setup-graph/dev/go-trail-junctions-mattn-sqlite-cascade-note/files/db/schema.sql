CREATE TABLE junction (
  id      TEXT PRIMARY KEY,
  name    TEXT NOT NULL,
  kind    TEXT NOT NULL CHECK (kind IN ('trailhead', 'fork', 'summit', 'hut')),
  elev_m  INTEGER
);

CREATE TABLE segment (
  id            INTEGER PRIMARY KEY,
  from_junction TEXT NOT NULL REFERENCES junction(id) ON DELETE CASCADE,
  to_junction   TEXT NOT NULL REFERENCES junction(id) ON DELETE CASCADE,
  km            REAL NOT NULL,
  surface       TEXT NOT NULL
);
CREATE INDEX segment_from ON segment(from_junction);
CREATE INDEX segment_to ON segment(to_junction);
