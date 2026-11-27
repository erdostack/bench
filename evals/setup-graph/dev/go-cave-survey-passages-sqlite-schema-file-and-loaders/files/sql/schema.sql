PRAGMA foreign_keys = ON;

CREATE TABLE station (
    id          TEXT PRIMARY KEY,
    name        TEXT,
    depth_m     REAL NOT NULL,
    survey_trip TEXT NOT NULL
);

CREATE TABLE passage (
    id           INTEGER PRIMARY KEY,
    from_station TEXT NOT NULL REFERENCES station (id),
    to_station   TEXT NOT NULL REFERENCES station (id),
    length_m     REAL NOT NULL,
    bearing      REAL,
    inclination  REAL
);

CREATE INDEX passage_from ON passage (from_station);
CREATE INDEX passage_to ON passage (to_station);
